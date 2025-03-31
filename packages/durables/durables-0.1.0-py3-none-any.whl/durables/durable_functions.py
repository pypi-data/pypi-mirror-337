import asyncio
from collections.abc import AsyncGenerator
import dataclasses
import json
import os
import random
from typing import Annotated, Any, Awaitable, Callable, Concatenate, Coroutine, Dict, Literal, TypeVar, Union
import typing
import uuid
import contextvars
import logging
import dill
import base64
from functools import wraps

from durables.persistence.protocol import ReplayableStreamProtocol, StreamViewProtocol
from .persistence.jsonl import JSONLStream
from pydantic import BaseModel, Field
from .models import DurableFunctionStep, DurableFunctionMessage, DurableFunctionEOS, DurableFunctionInputRequest, OrchestratorSettings


@dataclasses.dataclass
class OrchestratorSession:
    event_stream: StreamViewProtocol
    session_id: uuid.UUID
    inbox: ReplayableStreamProtocol
    outbox: ReplayableStreamProtocol
    step: int = 0
    settings: OrchestratorSettings = dataclasses.field(default_factory=OrchestratorSettings)

# Single context variable to store the orchestrator session
orchestrator_session = contextvars.ContextVar[OrchestratorSession]("orchestrator_session")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#TODO: emit() function and input() function with bytes as arguments as low level functions


# Decorator to create an ActivityFunction instance
def activity_function(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        session = orchestrator_session.get()
        if session is None:
            raise RuntimeError("No orchestrator_session set in context!")
        if session.event_stream is None:
            raise RuntimeError("No event_stream set in orchestrator session!")
        
        current_step = session.step
        stream = session.event_stream
        
        while True:
            try:
                event = await anext(stream)
            except StopAsyncIteration:
                break
            logger.debug("Comparing with event", event)
            if isinstance(event, DurableFunctionStep) and \
                event.kind == "activity" and \
                event.name == func.__name__ and \
                event.step == current_step:
                logger.info(f"[Replay] Skipping {func.__name__} (step {current_step}), result from store: {event.result}")
                session.step += 1  # Increment step
                return event.result  # Return cached result

        # Execute the function
        result = await func(*args, **kwargs)

        # Log the result
        await stream.put(
            DurableFunctionStep(
                name=func.__name__,
                step=session.step,
                result=result
            )
        )

        session.step += 1  # Increment step
        return result

    return wrapper


class NoInputMessageError(Exception):
    pass


@activity_function
async def _put_input_request(request_id: int, metadata: Dict[str, Any] | None = None) -> None:
    """Private activity function to publish input requests to the outbox stream."""
    session = orchestrator_session.get()
    if session is None:
        raise RuntimeError("No orchestrator_session set in context!")
    
    input_request = DurableFunctionInputRequest(
        request_id=request_id,
        metadata=metadata
    )
    
    await session.outbox.put(input_request)


@activity_function
async def input() -> bytes:
    session = orchestrator_session.get()
    if session is None:
        raise RuntimeError("No orchestrator_session set in context!")
    
    # Store the current step locally since it can change during execution
    current_step = session.step
    
    # Use wait_for_input from settings
    if session.settings.wait_for_input:
        inbox = session.inbox.iterate_blocking()
    else:
        inbox = session.inbox.iterate_nonblocking()
    
    # If publish_input_requests is enabled, publish an input request
    if session.settings.publish_input_requests:
        await _put_input_request(
            request_id=current_step,
            metadata={"step": current_step}
        )
    
    async for message in inbox:
        if not isinstance(message, DurableFunctionMessage):
            raise RuntimeError("Invalid message type")
        if message.id == current_step:
            return message.payload
    raise NoInputMessageError()


@activity_function
async def output(payload: bytes) -> None:
    session = orchestrator_session.get()
    if session is None:
        raise RuntimeError("No orchestrator_session set in context!")
    if not isinstance(payload, bytes):
        raise TypeError("Payload must be bytes")
    await session.outbox.put(
        DurableFunctionMessage(
            id = session.step,
            payload=payload
        )
    )


# Decorator to make a function an orchestrator function
def orchestrator_function(
        func: Callable[..., Coroutine[Any, Any, None]],
    ) -> Callable[Concatenate[uuid.UUID, ReplayableStreamProtocol, ReplayableStreamProtocol, OrchestratorSettings | None, ...], Coroutine[Any, Any, None]]:
    @wraps(func)
    async def wrapper(
        session_id: uuid.UUID,
        input_stream: ReplayableStreamProtocol,
        output_stream: ReplayableStreamProtocol,
        settings: OrchestratorSettings|None = None,
        *args: Any,
        **kwargs: Any
    ) -> None:
        stream = JSONLStream(str(session_id))
        
        # Use default settings if none provided
        if settings is None:
            settings = OrchestratorSettings()
        
        for i in range(settings.num_retries):
            # Create a new session with the event stream
            session = OrchestratorSession(
                session_id=session_id,
                step=0,
                event_stream=stream.iterate_nonblocking(),
                inbox=input_stream,
                outbox=output_stream,
                settings=settings
            )
            
            # Set the session in the context
            token = orchestrator_session.set(session)
            
            logger.info(f"Starting orchestrator: {func.__name__} (session: {session_id}, retry: {i})")

            try:
                await func(*args, **kwargs)
            except NoInputMessageError:
                raise
            except Exception as e:
                print(e)
                logger.exception(f"Orchestration error (session: {session_id}, retry: {i}): {e}")
                continue
            finally:
                orchestrator_session.reset(token)  # Restore the previous value
                
            logger.info(f"Orchestration complete (session: {session_id})")
            break

    return wrapper

