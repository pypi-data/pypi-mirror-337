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
from __future__ import annotations

import asyncio
import time
import typing as tp
from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse


from easydel.utils import traversals as etr
from easydel.utils.helpers import get_logger
from easydel.utils.lazy_import import is_package_available

from .api_models import (
	ChatCompletionRequest,
	ChatCompletionResponse,
	ChatCompletionResponseChoice,
	ChatCompletionStreamResponse,
	ChatCompletionStreamResponseChoice,
	ChatMessage,
	CountTokenRequest,
	DeltaMessage,
	UsageInfo,
)

if tp.TYPE_CHECKING:
	from .vinference import vInference, vInferenceConfig
else:
	vInference = tp.Any
	vInferenceConfig = tp.Any
TIMEOUT_KEEP_ALIVE = 5.0

APP = FastAPI()
logger = get_logger(__name__)


@etr.auto_pytree
class EndpointConfig:
	path: str
	handler: tp.Callable
	methods: list[str]
	summary: tp.Optional[str] = None
	tags: tp.Optional[list[str]] = None


def create_error_response(status_code: HTTPStatus, message: str) -> JSONResponse:
	return JSONResponse({"message": message}, status_code=status_code.value)


class vInferenceApiServer:
	def __init__(
		self,
		inference_map: tp.Union[tp.Dict[str, vInference], vInference] = None,
		inference_init_call: tp.Optional[tp.Callable[[], vInference]] = None,
		max_workers: int = 10,
	) -> None:
		from .vinference import vInference

		if inference_init_call is not None:
			inference_map = inference_init_call()

		assert inference_map is not None, "`inference_map` can not be None."
		if isinstance(inference_map, vInference):
			inference_map = {inference_map.inference_name: inference_map}
		for inference in inference_map.values():
			err_msg = "values and inferences in inference_map must be `vInference`"
			assert isinstance(inference, vInference), err_msg

		self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
		self.inference_map = inference_map

		self.logger = logger
		self.patch_endpoints()

	@property
	def _endpoints(self):
		return [
			EndpointConfig(
				path="/v1/chat/completions",
				handler=self.chat_completions,
				methods=["POST"],
				tags=["chat"],
				summary="Create a chat completion",
			),
			EndpointConfig(
				path="/liveness",
				handler=self.liveness,
				methods=["GET", "POST"],
				tags=["health"],
				summary="Check if ApiServer is up",
			),
			EndpointConfig(
				path="/readiness",
				handler=self.readiness,
				methods=["GET", "POST"],
				tags=["health"],
				summary="Check if ApiServer is ready",
			),
			EndpointConfig(
				path="/count_tokens",
				handler=self.count_tokens,
				methods=["POST"],
				tags=["utility"],
				summary="Count number of tokens with given inference runtime",
			),
			EndpointConfig(
				path="/available_inference",
				handler=self.available_inference,
				methods=["GET", "POST"],
				tags=["utility"],
				summary="Get available inference modules for requesting",
			),
		]

	async def chat_completions(self, request: ChatCompletionRequest):
		try:
			# Get model and tokenize input asynchronously
			inference = self._get_inference_model(request.model)
			ids = self._prepare_tokenized_input(request=request, inference=inference)
			if not request.stream:
				return await self._handle_non_streaming_response_async(request, inference, ids)
			else:
				return await self._handle_streaming_response(request, inference, ids)

		except Exception as e:
			return create_error_response(HTTPStatus.EXPECTATION_FAILED, str(e))

	def _get_inference_model(self, model_name: str) -> vInference:
		"""Get and validate inference model."""
		inference = self.inference_map.get(model_name)
		if inference is None:
			raise RuntimeError(f"Invalid model name: {model_name} is not available")
		return inference

	def _prepare_tokenized_input(
		self,
		request: ChatCompletionRequest,
		inference: vInference,
	) -> dict:
		"""Prepare tokenized input for the model."""

		conversation = request.model_dump()["messages"]

		return inference.processor_class.apply_chat_template(
			conversation=conversation,
			return_tensors="jax",
			add_generation_prompt=True,
			return_dict=True,
			tokenize=True,
			padding_side="left",
		)

	def _create_usage_info(
		self,
		prompt_tokens: int,
		ngenerated_tokens: int,
		processing_time: float,
		first_iter_flops: float,
		iter_flops: float,
		tokens_pre_second: float,
	) -> UsageInfo:
		"""Create usage information."""
		return UsageInfo(
			first_iter_flops=first_iter_flops,
			iter_flops=iter_flops,
			prompt_tokens=prompt_tokens,
			completion_tokens=ngenerated_tokens,
			total_tokens=ngenerated_tokens + prompt_tokens,
			tokens_pre_second=tokens_pre_second,
			processing_time=processing_time,
		)

	def _handle_non_streaming_response(
		self,
		request: ChatCompletionRequest,
		inference: vInference,
		ids: dict,
	) -> ChatCompletionResponse:
		"""Handle non-streaming response generation."""
		start = time.perf_counter()
		prompt_tokens = inference.count_tokens(request.model_dump()["messages"])
		# Generate response

		for response in inference.generate(**ids):
			pass  # Keep last response

		processing_time = time.perf_counter() - start

		final_responses = inference.tokenizer.batch_decode(
			response.sequences[..., response.padded_length :],
			skip_special_tokens=True,
		)

		# Determine finish reason
		finish_reason = (
			"length"
			if response.generated_tokens == inference.generation_config.max_new_tokens
			else "stop"
		)

		return ChatCompletionResponse(
			model=request.model,
			choices=[
				ChatCompletionResponseChoice(
					index=0,
					message=ChatMessage(role="assistant", content=final_response).model_dump(),
					finish_reason=finish_reason,
				)
				for final_response in final_responses
			],
			usage=self._create_usage_info(
				prompt_tokens,
				response.generated_tokens,
				processing_time,
				response.generate_func_flops,
				response.interval_func_flops,
				response.tokens_pre_second,
			),
		)

	async def _handle_non_streaming_response_async(self, request, inference, ids):
		response = await asyncio.get_event_loop().run_in_executor(
			self.thread_pool,
			self._handle_non_streaming_response,
			request,
			inference,
			ids,
		)
		return response

	async def _handle_streaming_response(
		self,
		request: ChatCompletionRequest,
		inference: vInference,
		ids: dict,
	) -> StreamingResponse:
		"""Handle streaming response generation asynchronously."""

		async def stream_results() -> tp.AsyncGenerator[bytes, tp.Any]:
			prompt_tokens = inference.count_tokens(request.model_dump()["messages"])
			start = time.perf_counter()

			# Create generator in thread pool to not block the event loop
			async def generate_tokens():
				return await asyncio.get_event_loop().run_in_executor(
					None,  # Use default thread pool
					inference.generate,
					**ids,
				)

			index = 0
			padded_sequence_length = None
			async for response in self._aiter_generator(await generate_tokens()):
				# Process each chunk asynchronously
				if padded_sequence_length is None:
					padded_sequence_length = response.padded_length
				next_slice = slice(
					padded_sequence_length,
					padded_sequence_length + inference.generation_config.streaming_chunks,
				)
				padded_sequence_length += inference.generation_config.streaming_chunks

				processing_time = time.perf_counter() - start

				# Decode tokens in thread pool to avoid blocking
				decoded_responses = await asyncio.get_event_loop().run_in_executor(
					None,
					inference.tokenizer.batch_decode,
					response.sequences[..., next_slice],
					True,  # skip_special_tokens
				)

				stream_resp = ChatCompletionStreamResponse(
					model=request.model,
					choices=[
						ChatCompletionStreamResponseChoice(
							index=index,
							delta=DeltaMessage(role="assistant", content=decoded_response),
							finish_reason=None,
						)
						for decoded_response in decoded_responses
					],
					usage=await self._create_usage_info_async(
						prompt_tokens,
						response.generated_tokens,
						processing_time,
						response.generate_func_flops,
						response.interval_func_flops,
						response.tokens_pre_second,
					),
				)
				index += 1
				yield ("data: " + stream_resp.model_dump_json() + "\n\n").encode("utf-8")

				# Add a small delay to prevent overwhelming the event loop
				await asyncio.sleep(0)

			# Final response with finish reason
			finish_reason = (
				"length"
				if response.generated_tokens == inference.generation_config.max_new_tokens
				else "stop"
			)
			stream_resp = ChatCompletionStreamResponse(
				model=request.model,
				choices=[
					ChatCompletionStreamResponseChoice(
						index=index,
						delta=DeltaMessage(role="assistant", content=""),
						finish_reason=finish_reason,
					)
					for i in decoded_responses
				],
				usage=await self._create_usage_info_async(
					prompt_tokens,
					response.generated_tokens,
					processing_time,
					response.generate_func_flops,
					response.interval_func_flops,
					response.tokens_pre_second,
				),
			)

			yield ("data: " + stream_resp.model_dump_json() + "\n\n").encode("utf-8")

		return StreamingResponse(stream_results(), media_type="text/event-stream")

	async def _aiter_generator(self, generator):
		"""Convert a regular generator to an async generator."""
		for item in generator:
			yield item
			# Give other coroutines a chance to run
			await asyncio.sleep(0)

	async def _create_usage_info_async(
		self,
		prompt_tokens: int,
		generated_tokens: int,
		processing_time: float,
		generate_flops: int,
		interval_flops: int,
		tokens_per_second: float,
	) -> dict:
		"""Async version of create_usage_info."""
		# If usage info calculation is CPU intensive, run it in thread pool
		return await asyncio.get_event_loop().run_in_executor(
			None,
			self._create_usage_info,
			prompt_tokens,
			generated_tokens,
			processing_time,
			generate_flops,
			interval_flops,
			tokens_per_second,
		)

	def liveness(self):
		return JSONResponse({"status": "ok"}, status_code=200)

	def readiness(self):
		return JSONResponse({"status": "ok"}, status_code=200)

	def available_inference(self):
		return JSONResponse(
			{"inference_map": list(self.inference_map.keys())},
			status_code=200,
		)

	def count_tokens(self, request: CountTokenRequest):
		try:
			conv = request.conversation
			model = request.model
			return JSONResponse(
				{"ntokens": self.inference_map[model].count_tokens(conv)},
				status_code=200,
			)
		except Exception as e:
			return create_error_response(HTTPStatus.EXPECTATION_FAILED, str(e))

	def patch_endpoints(self):
		"""Register all endpoints with the FastAPI app."""
		for endpoint in self._endpoints:
			for method in endpoint.methods:
				route_params = {
					"path": endpoint.path,
					"response_model": None,
				}
				if endpoint.summary:
					route_params["summary"] = endpoint.summary
				if endpoint.tags:
					route_params["tags"] = endpoint.tags
				if method == "GET":
					APP.get(**route_params)(endpoint.handler)
				elif method == "POST":
					APP.post(**route_params)(endpoint.handler)

	def fire(
		self,
		host="0.0.0.0",
		port=11556,
		metrics_port: tp.Optional[int] = None,
		log_level="debug",
	):
		metrics_port = metrics_port or (port + 1)
		if is_package_available("prometheus_client"):
			from prometheus_client import start_http_server  # type:ignore

			start_http_server(metrics_port)

		uvicorn.run(
			APP,
			host=host,
			port=port,
			log_level=log_level,
			timeout_keep_alive=TIMEOUT_KEEP_ALIVE,
			loop="uvloop",
		)
