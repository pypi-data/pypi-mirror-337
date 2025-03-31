import contextvars
import uuid
import pytest
import asyncio
from unittest.mock import patch
from durables.durable_functions import (
    NoInputMessageError,
    orchestrator_function,
    activity_function, 
    orchestrator_session,
    input,
    output,
    OrchestratorSession)
from durables.models import DurableFunctionMessage, OrchestratorSettings
from durables.persistence.jsonl import JSONLStream

@pytest.fixture
def temp_file_path(tmp_path):
    return tmp_path / "test_stream.jsonl"

@pytest.fixture
async def stream(temp_file_path):
    return JSONLStream("test_stream", temp_file_path.parent)

@pytest.fixture
async def inbox_stream(temp_file_path):
    return JSONLStream("inbox_stream", temp_file_path.parent)

@pytest.fixture
async def outbox_stream(temp_file_path):
    return JSONLStream("outbox_stream", temp_file_path.parent)


async def test_activity_function_replay(stream):
    call_count = contextvars.ContextVar("call_count", default=0)
    call_count.set(0)
    @activity_function
    async def mock_activity(x):
        call_count.set(call_count.get() + 1)
        await asyncio.sleep(0.1)
        return x * 2
    
    # Create and set the orchestrator session
    session = OrchestratorSession(
        session_id="test_session",
        step=0,
        event_stream=stream.iterate_nonblocking(),
        inbox=stream,
        outbox=stream
    )
    orchestrator_session.set(session)

    # First run: execute and store result
    result = await mock_activity(10)
    assert result == 20
    
    # Reset step for second run
    session.step = 0
    
    # Second run: should replay result
    result = await mock_activity(10)
    assert result == 20

    # Verify call count
    assert call_count.get() == 1


test_count = 0
@pytest.mark.asyncio
async def test_orchestrator_function_retries():
    @activity_function
    async def maybe_failing_activity(x):
        global test_count
        await asyncio.sleep(.1)  # Simulate work
        test_count += 1
        if test_count %2 == 1:
            raise RuntimeError("Task B failed due to coin flip")
        return f"{x}"

    @orchestrator_function
    async def orchestrator():
        result_a = await maybe_failing_activity(10)
        result_b = await maybe_failing_activity(20)
        result_c = await maybe_failing_activity(30)
        result = result_a + result_b + result_c
        assert result == "102030"

    session_id = uuid.uuid4()
    input_stream = JSONLStream(uuid.uuid4())#.iterate_nonblocking()
    output_stream = JSONLStream(uuid.uuid4())#.iterate_nonblocking()
    await orchestrator(session_id, input_stream, output_stream)



async def test_input_function_fail_on_wait(inbox_stream, outbox_stream):
    @orchestrator_function
    async def orchestrator():
        a = await input()
        b = await input()
        await output(a + b" " +b)
    session_id = uuid.uuid4()
    with pytest.raises(NoInputMessageError):
        await orchestrator(
            session_id=session_id,
            input_stream=inbox_stream,
            output_stream=outbox_stream,
            settings=OrchestratorSettings(
                wait_for_input=False,
                publish_input_requests=False
            )
        )
    await inbox_stream.put(DurableFunctionMessage(id=0, payload=b"Hello"))
    await inbox_stream.put(DurableFunctionMessage(id=1, payload=b"World"))
    await orchestrator(
        session_id=session_id,
        input_stream=inbox_stream,
        output_stream=outbox_stream,
        settings=OrchestratorSettings(
            wait_for_input=False,
            publish_input_requests=False
        )
    )
    result = await anext(aiter(outbox_stream.iterate_blocking()))
    assert result.id == 2
    assert result.payload == b"Hello World"


async def test_input_function_wait(inbox_stream, outbox_stream):
    @orchestrator_function
    async def orchestrator():
        a = await input()
        b = await input()
        await output(a + b" " +b)
    orchestrator_task = asyncio.create_task(
        orchestrator(
            session_id=uuid.uuid4(),
            input_stream=inbox_stream,
            output_stream=outbox_stream,
            settings=OrchestratorSettings(
                wait_for_input=True,
                publish_input_requests=False
            )
        )
    )
    await asyncio.sleep(0.1)
    await inbox_stream.put(DurableFunctionMessage(id=0, payload=b"Hello"))
    await asyncio.sleep(0.1)
    await inbox_stream.put(DurableFunctionMessage(id=1, payload=b"World"))
    result = await anext(aiter(outbox_stream.iterate_blocking()))
    assert result.id == 2
    assert result.payload == b"Hello World"
    await orchestrator_task


async def test_input_function_with_publish_requests(inbox_stream, outbox_stream):
    @orchestrator_function
    async def orchestrator():
        a = await input()
        b = await input()
        await output(a + b" " + b)
    
    # Start the orchestrator with publish_input_requests=True
    orchestrator_task = asyncio.create_task(
        orchestrator(
            session_id=uuid.uuid4(),
            input_stream=inbox_stream,
            output_stream=outbox_stream,
            settings=OrchestratorSettings(
                wait_for_input=True,
                publish_input_requests=True
            )
        )
    )

    
    # Read the input request from outbox
    outbox_iterator = outbox_stream.iterate_blocking()
    first_message = await anext(outbox_iterator)
    
    # Verify it's an input request and has the correct request_id
    assert first_message.kind == "input_request"
    assert first_message.request_id == 0
    assert "step" in first_message.metadata
    
    # Respond with a message matching the request_id
    await inbox_stream.put(DurableFunctionMessage(id=first_message.request_id, payload=b"Hello"))
    
    # Wait for the second input request
    second_message = await anext(outbox_iterator)
    assert second_message.kind == "input_request"
    assert second_message.request_id == 2
    
    # Respond to the second request
    await inbox_stream.put(DurableFunctionMessage(id=second_message.request_id, payload=b"World"))
    
    # Verify the final output message
    final_message = await anext(outbox_iterator)
    assert final_message.kind == "message"
    assert final_message.id == 4
    assert final_message.payload == b"Hello World"
    
    # Make sure the orchestrator completes
    await orchestrator_task

