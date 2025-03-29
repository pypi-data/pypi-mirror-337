from typing import Any

from litellm import acompletion, completion
from litellm.exceptions import RateLimitError, ServiceUnavailableError
from pydantic import BaseModel

from aikernel.errors import ModelUnavailableError, NoResponseError, RateLimitExceededError
from aikernel._internal.types.provider import LiteLLMMessage
from aikernel._internal.types.request import (
    LLMAssistantMessage,
    LLMModel,
    LLMSystemMessage,
    LLMTool,
    LLMToolMessage,
    LLMUserMessage,
)
from aikernel._internal.types.response import LLMResponseUsage, LLMStructuredResponse

AnyLLMTool = LLMTool[Any]


def llm_structured_sync[T: BaseModel](
    *,
    messages: list[LLMUserMessage | LLMAssistantMessage | LLMSystemMessage | LLMToolMessage],
    model: LLMModel,
    response_model: type[T],
) -> LLMStructuredResponse[T]:
    rendered_messages: list[LiteLLMMessage] = []
    for message in messages:
        if isinstance(message, LLMToolMessage):
            invocation_message, response_message = message.render_call_and_response()
            rendered_messages.append(invocation_message)
            rendered_messages.append(response_message)
        else:
            rendered_messages.append(message.render())

    try:
        response = completion(messages=rendered_messages, model=model.value, response_format=response_model)
    except ServiceUnavailableError:
        raise ModelUnavailableError()
    except RateLimitError:
        raise RateLimitExceededError()

    if len(response.choices) == 0:
        raise NoResponseError()

    text = response.choices[0].message.content
    usage = LLMResponseUsage(input_tokens=response.usage.prompt_tokens, output_tokens=response.usage.completion_tokens)

    return LLMStructuredResponse(text=text, structure=response_model, usage=usage)


async def llm_structured[T: BaseModel](
    *,
    messages: list[LLMUserMessage | LLMAssistantMessage | LLMSystemMessage | LLMToolMessage],
    model: LLMModel,
    response_model: type[T],
) -> LLMStructuredResponse[T]:
    rendered_messages: list[LiteLLMMessage] = []
    for message in messages:
        if isinstance(message, LLMToolMessage):
            invocation_message, response_message = message.render_call_and_response()
            rendered_messages.append(invocation_message)
            rendered_messages.append(response_message)
        else:
            rendered_messages.append(message.render())

    try:
        response = await acompletion(messages=rendered_messages, model=model.value, response_format=response_model)
    except ServiceUnavailableError:
        raise ModelUnavailableError()
    except RateLimitError:
        raise RateLimitExceededError()

    if len(response.choices) == 0:
        raise NoResponseError()

    text = response.choices[0].message.content
    usage = LLMResponseUsage(input_tokens=response.usage.prompt_tokens, output_tokens=response.usage.completion_tokens)

    return LLMStructuredResponse(text=text, structure=response_model, usage=usage)
