from uuid import uuid4
import pytest
import asyncio
import nats
from durables.models import DurableFunctionStep
from durables.persistence.nats import NatsStream, custom_serializer, custom_loader
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
import os
from functools import partial

# Configure pytest to skip tests if NATS is not available
pytestmark = pytest.mark.asyncio

# @pytest.fixture(scope="module")
# async def nats_server():
#     """Real NATS connection for testing."""
#     try:
#         nc = await nats.connect("nats://localhost:4222")
#         yield nc
#         await nc.close()
#     except Exception as e:
#         pytest.skip(f"NATS server not available: {e}")

@pytest.fixture
async def stream():
    """Create a NatsStream instance with real NATS connection"""
    stream_name = f"{uuid4().hex}"  # Unique stream name
    print("STREAM", stream_name)
    stream = NatsStream(stream_name)
    yield stream
    if stream.nc is not None and stream.nc.is_connected:
        await stream.nc.close()  # Close the NATS connection after tests
    # # # Cleanup
    # try:
    #     await stream.js.delete_stream(stream_name)
    # except:
    #     pass  # Ignore cleanup errors

async def test_put_and_iter_stream(stream):
    # Test putting and iterating over events
    events = [DurableFunctionStep(step=i, result=i, name="test") for i in range(5)]
    for event in events:
        await stream.put(event)
    await stream.close()

    read_events = []
    async for item in stream.iterate_blocking():
        read_events.append(item)
        print(item)
    
    assert len(read_events) == 5
    for i in range(5):
        assert read_events[i].result == i
    

async def test_custom_serializer_and_loader():
    event = DurableFunctionStep(step=0, result=42, name="test")
    serialized_event = custom_serializer(event)
    assert "result_preview" in serialized_event
    assert serialized_event["result_preview"] == "42"
    
    loaded_event = custom_loader(serialized_event)
    assert "result_preview" not in loaded_event
    assert loaded_event.result == 42

async def test_concurrent_read_write(stream):
    async def writer():
        for i in range(5):
            await stream.put(DurableFunctionStep(step=i, result=i, name="test"))
            await asyncio.sleep(0.01)
        await stream.close()

    async def reader():
        read_events = []
        async for item in stream.iterate_blocking():
            read_events.append(item)
        return read_events

    writer_task = asyncio.create_task(writer())
    reader_task = asyncio.create_task(reader())

    await writer_task
    read_events = await reader_task

    assert len(read_events) == 5
    for i in range(5):
        assert read_events[i].result == i

async def test_replay_mechanism(stream):
    events = [DurableFunctionStep(step=i, result=i, name="test") for i in range(6)]
    
    for event in events:
        await stream.put(event)
    await stream.close()
    
    read_events1 = []
    async for item in stream.iterate_blocking():
        read_events1.append(item)

    read_events2 = []
    async for item in stream.iterate_blocking():
        read_events2.append(item)
    print(read_events1)
    assert len(read_events1) == len(events)
    assert len(read_events2) == len(events)
    for i in range(3):
        assert read_events1[i].step == read_events2[i].step
        assert read_events1[i].result == read_events2[i].result
        assert read_events1[i].name == read_events2[i].name


async def test_next(stream):
    events = [DurableFunctionStep(step=i, result=i, name="test") for i in range(5)]
    for event in events:
        await stream.put(event)
    await stream.close()
    aiterator = aiter(stream.iterate_blocking())
    for i in range(5):
        item = await anext(aiterator)
        assert item.result == i

async def test_next_nowait(stream):
    events = [DurableFunctionStep(step=i, result=i, name="test") for i in range(5)]
    for event in events:
        await stream.put(event)
    await stream.close()
    i = 0
    async for item in stream.iterate_nonblocking():
        assert item.result == i
        i += 1

async def test_next_nowait_with_delay(stream):
    async def delayed_put():
        await asyncio.sleep(0.2)
        await stream.put(DurableFunctionStep(step=0, result=0, name="test"))
        await stream.close()

    asyncio.create_task(delayed_put())
    aiterator = aiter(stream.iterate_nonblocking())
    with pytest.raises(StopAsyncIteration):
        item = await anext(aiterator)

    # await asyncio.sleep(1)
    await asyncio.sleep(.3)
    aiterator = aiter(stream.iterate_nonblocking())
    item = await anext(aiterator)

    assert item.result == 0

async def test_threaded_read_write(stream):
    stream_name = stream.stream_name
    
    def writer():
        async def write():
            local_stream = NatsStream(stream_name)
            for i in range(5):
                await local_stream.put(DurableFunctionStep(step=i, result=i, name="test"))
                await asyncio.sleep(0.01)
            await local_stream.close()
            await local_stream.nc.close()
        asyncio.run(write())

    def reader():
        read_events = []
        async def read():
            local_stream = NatsStream(stream_name)
            async for item in local_stream.iterate_blocking():
                read_events.append(item)
            await local_stream.nc.close()

        asyncio.run(read())
        return read_events

    # Run the writer and reader in separate threads
    with ThreadPoolExecutor(max_workers=2) as executor:
        writer_future = executor.submit(writer)
        reader_future = executor.submit(reader)

    writer_future.result()
    read_events = reader_future.result()

    assert len(read_events) == 5
    for i in range(5):
        assert read_events[i].result == i

def writer_process(stream_name):
    async def do():
        stream = NatsStream(stream_name)
        for i in range(5):
            await stream.put(DurableFunctionStep(step=i, result=i, name="test"))
            await asyncio.sleep(0.01)
        await stream.close()
    asyncio.run(do())

def reader_process(stream_name):
    read_events = []
    async def read():
        stream = NatsStream(stream_name)
        async for item in stream.iterate_blocking():
            read_events.append(item)
            # Convert to dict to make it serializable for multiprocessing
            serialized = {"step": item.step, "result": item.result, "name": item.name}
            read_events[-1] = serialized
    asyncio.run(read())
    return read_events

async def test_process_read_write(stream):
    stream_name = stream.stream_name
    
    with ProcessPoolExecutor() as executor:
        writer_future = executor.submit(writer_process, stream_name)
        # Give writer a chance to start
        await asyncio.sleep(0.1)
        reader_future = executor.submit(reader_process, stream_name)
        reader_future2 = executor.submit(reader_process, stream_name)

    writer_future.result()
    read_events = reader_future.result()
    read_events2 = reader_future2.result()

    assert len(read_events) == 5
    assert len(read_events2) == 5
    for i in range(5):
        assert read_events[i]["result"] == i
        assert read_events2[i]["result"] == i
