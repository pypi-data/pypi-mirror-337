# Copyright 2023 The EASYDEL Author @erfanzar (Erfan Zare Chavoshi).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import typing as tp
from functools import cached_property, partial

import chex
import jax
import jax.numpy as jnp
from flax import nnx as nn

from easydel.infra.base_module import EasyDeLBaseModule
from easydel.infra.factory import TaskType, register_module
from easydel.infra.modeling_outputs import (
	FlaxBaseModelOutput,
	FlaxCausalLMOutput,
)
from easydel.infra.utils import (
	ACT2FN,
	auto_remat,
	block_wise_ffn,
	control_mlp_sharding,
	get_dot_general_by_bits,
)
from easydel.layers.attention import FlaxAttentionModule, FlexibleAttentionModule
from easydel.layers.caching import TransformerCache, TransformerCacheView
from easydel.modules.stablelm.stablelm_configuration import (
	StableLmConfig as StableLmConfig,
)


class StableLmMLP(nn.Module):
	def __init__(
		self,
		config: StableLmConfig,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	):
		self.config = config
		self.dtype = dtype
		self.param_dtype = param_dtype
		self.precision = precision
		linear_class = partial(
			nn.Linear,
			dtype=dtype,
			param_dtype=param_dtype,
			use_bias=False,
			kernel_init=jax.nn.initializers.normal(config.initializer_range),
			precision=precision,
			**get_dot_general_by_bits(config.bits, config.easy_method),
		)

		self.gate_proj = linear_class(
			config.hidden_size,
			config.intermediate_size,
			rngs=rngs,
		)
		self.down_proj = linear_class(
			config.intermediate_size,
			config.hidden_size,
			rngs=rngs,
		)
		self.up_proj = linear_class(
			config.hidden_size,
			config.intermediate_size,
			rngs=rngs,
		)
		self.act_fn = ACT2FN[config.hidden_act]

	def __call__(self, hidden_states: jnp.ndarray) -> jnp.ndarray:
		hidden_states = control_mlp_sharding(hidden_states, self.config.partition_axis)

		return self.down_proj(
			self.act_fn(self.gate_proj(hidden_states)) * self.up_proj(hidden_states)
		)


class StableLmLayerNormPerHead(nn.Module):
	def __init__(
		self,
		head_dim: int,
		num_heads: int,
		eps: float = 1e-5,
		bias: bool = False,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		*,
		rngs: nn.Rngs,
	):
		self.norms = [
			nn.LayerNorm(
				head_dim,
				epsilon=eps,
				use_bias=bias,
				dtype=dtype,
				param_dtype=param_dtype,
				rngs=rngs,
			)
			for idx in range(num_heads)
		]

	def __call__(self, hidden_states):
		states_per_heads = jnp.split(hidden_states, 1, axis=1)
		# Normalize and merge the heads back together
		return jnp.concatenate(
			[
				norm(hidden_states) for norm, hidden_states in zip(self.norms, states_per_heads)
			],
			axis=1,
		)


class StableLmAttention(FlaxAttentionModule):
	def __init__(
		self,
		config: StableLmConfig,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	):
		super().__init__(config=config)
		self.dtype = dtype
		self.param_dtype = param_dtype
		self.precision = precision
		self.rngs = rngs
		self.hidden_size = config.hidden_size
		self.num_heads = config.num_attention_heads
		self.head_dim = self.hidden_size // self.num_heads
		self.num_key_value_heads = config.num_key_value_heads
		self.num_key_value_groups = self.num_heads // self.num_key_value_heads
		self.max_position_embeddings = config.max_position_embeddings
		self.rope_theta = config.rope_theta
		self.partial_rotary_factor = config.partial_rotary_factor

		if self.num_key_value_groups == 1:
			assert self.config.num_attention_heads == self.config.num_key_value_heads

		linear_class = partial(
			nn.Linear,
			dtype=dtype,
			param_dtype=param_dtype,
			kernel_init=jax.nn.initializers.normal(config.initializer_range),
			precision=precision,
			**get_dot_general_by_bits(config.bits, config.easy_method),
		)
		self.q_proj = linear_class(
			config.hidden_size,
			config.num_attention_heads * self.head_dim,
			use_bias=self.config.use_qkv_bias,
			rngs=rngs,
		)
		self.k_proj = linear_class(
			config.hidden_size,
			config.num_key_value_heads * self.head_dim,
			use_bias=self.config.use_qkv_bias,
			rngs=rngs,
		)
		self.v_proj = linear_class(
			config.hidden_size,
			config.num_key_value_heads * self.head_dim,
			use_bias=self.config.use_qkv_bias,
			rngs=rngs,
		)
		self.o_proj = linear_class(
			config.num_attention_heads * self.head_dim,
			config.hidden_size,
			use_bias=False,
			rngs=rngs,
		)

		self.rotary_emb_dim = int(self.config.partial_rotary_factor * self.head_dim)
		self.attention_performer = FlexibleAttentionModule(
			base_config=config,
			softmax_scale=self.head_dim**-0.5,
			dropout_prob=config.attention_dropout,
		)

		self.qk_layernorm = config.qk_layernorm
		if self.qk_layernorm:
			self.q_layernorm = StableLmLayerNormPerHead(
				head_dim=self.head_dim,
				num_heads=config.num_attention_heads,
				eps=config.layer_norm_eps,
				dtype=self.dtype,
				param_dtype=self.param_dtype,
				rngs=rngs,
			)
			self.k_layernorm = StableLmLayerNormPerHead(
				head_dim=self.head_dim,
				num_heads=config.num_key_value_heads,
				eps=config.layer_norm_eps,
				dtype=self.dtype,
				param_dtype=self.param_dtype,
				rngs=rngs,
			)

		self.rotary = self.config.get_basic_rope(
			self.dtype,
			head_size=int(
				config.partial_rotary_factor
				* (config.hidden_size // config.num_attention_heads)
			),
			rotary_dim=self.rotary_emb_dim,
			base=config.rope_theta,
		)

	def __call__(
		self,
		hidden_states: chex.Array,
		attention_mask: chex.Array,
		position_ids: chex.Array,
		causal_mask: chex.Array,
		cache_view: tp.Optional[TransformerCacheView] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		output_attentions: bool = False,
		fcm_mask: tp.Optional[chex.Array] = None,
		frequencies: tp.Optional[chex.Array] = None,
	):
		batch_size, sequence_length = hidden_states.shape[:2]
		query_states, key_states, value_states = (
			self.q_proj(hidden_states),
			self.k_proj(hidden_states),
			self.v_proj(hidden_states),
		)

		query_states = query_states.reshape(
			batch_size,
			sequence_length,
			self.config.num_attention_heads,
			self.head_dim,
		)
		key_states = key_states.reshape(
			batch_size,
			sequence_length,
			self.config.num_key_value_heads,
			self.head_dim,
		)
		value_states = value_states.reshape(
			batch_size,
			sequence_length,
			self.config.num_key_value_heads,
			self.head_dim,
		)

		if self.qk_layernorm:
			query_states = self.q_layernorm(query_states.transpose(0, 2, 1, 3)).transpose(
				0, 2, 1, 3
			)
			key_states = self.k_layernorm(key_states.transpose(0, 2, 1, 3)).transpose(
				0, 2, 1, 3
			)

		query_states, key_states = self.rotary(
			positions=position_ids,
			query=query_states,
			key=key_states,
			frequencies=frequencies,
		)

		(
			key_states,
			value_states,
			attention_mask,
			init_attention_bias,
		) = self.concatenate(
			query=query_states,
			key=key_states,
			cache_view=cache_view,
			value=value_states,
			attention_mask=attention_mask,
			causal_mask=causal_mask,
			fcm_mask=fcm_mask,
		)

		attentions = self.attention_performer.forward(
			query_states=query_states,
			key_states=key_states,
			value_states=value_states,
			bias=None,
			init_bias=init_attention_bias,
			attention_mask=attention_mask,
			segment_ids=segment_ids,
			causal=True,
			dropout_rng=self.rngs.params(),
		)

		attn_output = self.shard_attention_prod(
			self._merge_heads(attentions.attention_outputs)
		)
		attn_output = self.o_proj(attn_output)
		outputs = (
			(attn_output, attentions.attention_weights)
			if output_attentions
			else (attn_output,)
		)
		return outputs


class StableLmDecoderLayer(nn.Module):
	def __init__(
		self,
		config: StableLmConfig,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	):
		self.config = config
		self.dtype = dtype
		self.param_dtype = param_dtype
		self.precision = precision
		attn_block = StableLmAttention
		mlp_block = StableLmMLP
		self.use_parallel_residual = self.config.use_parallel_residual
		attn_block, mlp_block = auto_remat(
			attn_block,
			mlp_block,
			policy=config.gradient_checkpointing,
		)
		self.self_attn = attn_block(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.mlp = mlp_block(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.input_layernorm = nn.LayerNorm(
			config.hidden_size,
			epsilon=config.layer_norm_eps,
			dtype=dtype,
			param_dtype=param_dtype,
			rngs=rngs,
		)
		if not self.use_parallel_residual:
			self.post_attention_layernorm = nn.LayerNorm(
				config.hidden_size,
				epsilon=config.layer_norm_eps,
				dtype=dtype,
				param_dtype=param_dtype,
				rngs=rngs,
			)
		self.dropout = nn.Dropout(self.config.hidden_dropout, rngs=rngs)

	def __call__(
		self,
		hidden_states: chex.Array,
		attention_mask: chex.Array,
		position_ids: chex.Array,
		causal_mask: chex.Array,
		cache_view: tp.Optional[TransformerCacheView] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		output_attentions: bool = False,
		fcm_mask: tp.Optional[chex.Array] = None,
		frequencies: tp.Optional[chex.Array] = None,
	):
		residual = hidden_states
		hidden_states = self.input_layernorm(hidden_states)
		attn_out = self.self_attn(
			hidden_states,
			attention_mask,
			position_ids,
			causal_mask,
			cache_view,
			segment_ids,
			output_attentions,
			fcm_mask,
			frequencies,
		)
		attn_out, self_attn_weights = (
			(attn_out[0], attn_out[1]) if len(attn_out) == 2 else (attn_out[0], None)
		)

		if self.use_parallel_residual:
			if self.config.use_scan_mlp:
				hidden_states = block_wise_ffn(
					self.mlp, hidden_states, self.config.scan_mlp_chunk_size
				)
			else:
				hidden_states = self.mlp(hidden_states)

			hidden_states = self.dropout(hidden_states)
			hidden_states = hidden_states + residual + attn_out
		else:
			residual = residual + attn_out
			if self.config.use_scan_mlp:
				hidden_states = block_wise_ffn(
					self.mlp,
					self.post_attention_layernorm(residual),
					self.config.scan_mlp_chunk_size,
				)
			else:
				hidden_states = self.mlp(self.post_attention_layernorm(residual))
			hidden_states = self.dropout(hidden_states)
			hidden_states = hidden_states + residual
		outputs = (hidden_states,)

		if output_attentions:
			outputs += (self_attn_weights,)

		return outputs


@register_module(
	TaskType.BASE_MODULE,
	config=StableLmConfig,
	model_type="stablelm",
)
class StableLmModel(EasyDeLBaseModule):
	def __init__(
		self,
		config: StableLmConfig,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	):
		super().__init__(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)

		self.padding_idx = config.pad_token_id
		self.vocab_size = config.vocab_size

		self.embed_tokens = nn.Embed(
			config.vocab_size,
			config.hidden_size,
			dtype=dtype,
			param_dtype=param_dtype,
			rngs=rngs,
		)
		self.layers = [
			StableLmDecoderLayer(
				config=config,
				dtype=dtype,
				param_dtype=param_dtype,
				precision=precision,
				rngs=rngs,
			)
			for idx in range(config.num_hidden_layers)
		]

		self.norm = nn.LayerNorm(
			config.hidden_size,
			epsilon=config.layer_norm_eps,
			dtype=dtype,
			param_dtype=param_dtype,
			rngs=rngs,
		)

	@cached_property
	def frequencies(self):
		rotary_emb_dim = int(
			self.config.partial_rotary_factor
			* (self.config.hidden_size // self.config.num_attention_heads)
		)
		self._frequencies = self.config.get_basic_frequencies(
			head_size=rotary_emb_dim,
			rotary_dim=rotary_emb_dim,
		)

	def __call__(
		self,
		input_ids: tp.Optional[chex.Array] = None,
		inputs_embeds: tp.Optional[chex.Array] = None,
		attention_mask: tp.Optional[chex.Array] = None,
		position_ids: tp.Optional[chex.Array] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		output_attentions: tp.Optional[bool] = None,
		output_hidden_states: tp.Optional[bool] = None,
		past_key_values: tp.Optional[TransformerCache] = None,
		return_dict: bool = True,
	) -> tp.Union[FlaxBaseModelOutput, tp.Tuple]:
		"""
		Forward pass through the StableLm module.

		Args:
		    input_ids (chex.Array): Input tensor containing token IDs.
		    attention_mask (chex.Array): Mask for attention.
		    position_ids (chex.Array): Positional indices.
		    segment_ids (tp.Optional[chex.Array]): Segment IDs for different input parts.
		    inputs_embeds (tp.Optional[chex.Array]): Embedded input tensor.
		    output_attentions (tp.Optional[bool]): If True, output attention weights.
		    output_hidden_states (tp.Optional[bool]): If True, output hidden states.
		    init_cache (bool): If True, initialize cache for decoding.
		    deterministic (bool): If True, disable dropout.
		    return_dict (bool): If True, return a dictionary of outputs.

		Returns:
		    FlaxBaseModelOutput | tp.Tuple: Model output, either as a named tuple or a standard tuple.
		"""
		if (input_ids is None) ^ (inputs_embeds is not None):
			raise ValueError(
				"You cannot specify both input_ids and inputs_embeds at the same time, and must specify either one"
			)
		if inputs_embeds is None:
			inputs_embeds = self.embed_tokens(input_ids.astype("i4"))
		batch_size, sequence_length, _ = inputs_embeds.shape

		all_attentions = () if output_attentions else None
		all_hidden_states = () if output_hidden_states else None
		assert sequence_length <= self.config.max_position_embeddings, (
			f"Maximum Position Embedding Reached ! (Excepted <= {self.config.max_position_embeddings} got {sequence_length})"
		)
		if attention_mask is None:
			attention_mask = jnp.ones((batch_size, sequence_length), "b1")
		else:
			if attention_mask.dtype != jnp.bool:
				attention_mask = jnp.astype(attention_mask == 1, "b1")
		if position_ids is None:
			position_ids = jnp.broadcast_to(
				jnp.clip(jnp.cumsum(attention_mask, axis=-1) - 1, a_min=0),
				(batch_size, sequence_length),
			).astype(jnp.int32)
		if attention_mask.ndim == 2:
			attention_mask = jnp.expand_dims(attention_mask, (1, 2))
		hidden_states = inputs_embeds

		if past_key_values is None:
			past_key_values = TransformerCache.init_empty(len(self.layers))
		for idx, block in enumerate(self.layers):
			if output_hidden_states:
				all_hidden_states += (hidden_states,)

			layer_outputs = block(
				hidden_states=hidden_states,
				attention_mask=attention_mask,
				position_ids=position_ids,
				cache_view=past_key_values.views[idx],
				causal_mask=self.causal_mask,
				output_attentions=output_attentions,
				segment_ids=segment_ids,
				frequencies=self.frequencies,
			)
			hidden_states = layer_outputs[0]

			if output_attentions:
				all_attentions += (layer_outputs[1],)

		hidden_states = self.norm(hidden_states)

		if output_hidden_states:
			all_hidden_states += (hidden_states,)
		outputs = (hidden_states, all_hidden_states, all_attentions, past_key_values)

		if not return_dict:
			return tuple(value for value in outputs if value is not None)

		return FlaxBaseModelOutput(
			last_hidden_state=hidden_states,
			hidden_states=all_hidden_states,
			attentions=all_attentions,
			past_key_values=past_key_values,
		)


@register_module(
	TaskType.CAUSAL_LM,
	config=StableLmConfig,
	model_type="stablelm",
)
class StableLmForCausalLM(EasyDeLBaseModule):
	def __init__(
		self,
		config: StableLmConfig,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	):
		super().__init__(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.model = StableLmModel(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.vocab_size = self.config.vocab_size
		self.lm_head = nn.Linear(
			config.hidden_size,
			config.vocab_size,
			use_bias=False,
			kernel_init=jax.nn.initializers.normal(config.initializer_range),
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)

	def __call__(
		self,
		input_ids: tp.Optional[chex.Array] = None,
		inputs_embeds: tp.Optional[chex.Array] = None,
		attention_mask: tp.Optional[chex.Array] = None,
		position_ids: tp.Optional[chex.Array] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		output_attentions: tp.Optional[bool] = None,
		output_hidden_states: tp.Optional[bool] = None,
		past_key_values: tp.Optional[TransformerCache] = None,
		return_dict: bool = True,
	) -> tp.Union[FlaxCausalLMOutput, tp.Tuple]:
		outputs = self.model(
			input_ids=input_ids,
			attention_mask=attention_mask,
			position_ids=position_ids,
			output_attentions=output_attentions,
			output_hidden_states=output_hidden_states,
			past_key_values=past_key_values,
			return_dict=return_dict,
			inputs_embeds=inputs_embeds,
			segment_ids=segment_ids,
		)
		hidden_states = outputs[0]

		if self.config.tie_word_embeddings:
			lm_logits = jax.lax.dot_general(
				hidden_states,
				self.model.embed_tokens.embedding.value.T,
				(((hidden_states.ndim - 1), (0,)), ((), ())),
			)
		else:
			lm_logits = self.lm_head(hidden_states)

		if not return_dict:
			return (lm_logits,) + outputs[1:]

		return FlaxCausalLMOutput(
			logits=lm_logits,
			hidden_states=outputs.hidden_states,
			attentions=outputs.attentions,
			past_key_values=outputs.past_key_values,
		)
