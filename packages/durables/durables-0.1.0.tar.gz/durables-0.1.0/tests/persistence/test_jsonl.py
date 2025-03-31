import pytest
import asyncio
from durables.models import DurableFunctionStep
from durables.persistence.jsonl import JSONLStream, custom_serializer, custom_loader
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

@pytest.fixture
def temp_file_path(tmp_path):
    return tmp_path / "test_stream.jsonl"

@pytest.fixture
async def stream(temp_file_path):
    return JSONLStream("test_stream", temp_file_path.parent)


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
    

    assert len(read_events1) == 6
    assert len(read_events2) == 6
    for i in range(3):
        assert read_events1[i].step == read_events2[i].step
        assert read_events1[i].result == read_events2[i].result
        assert read_events1[i].name == read_events2[i].name

async def test_threaded_read_write(temp_file_path):
    def writer():
        stream = JSONLStream("test_stream", temp_file_path.parent)
        for i in range(5):
            asyncio.run(stream.put(DurableFunctionStep(step=i, result=i, name="test")))
        asyncio.run(stream.close())

    def reader():
        stream = JSONLStream("test_stream", temp_file_path.parent)
        read_events = []
        async def read():
            async for item in stream.iterate_blocking():
                read_events.append(item)
        asyncio.run(read())
        return read_events

    with ThreadPoolExecutor() as executor:
        writer_future = executor.submit(writer)
        reader_future = executor.submit(reader)

    writer_future.result()
    read_events = reader_future.result()

    assert len(read_events) == 5
    for i in range(5):
        assert read_events[i].result == i

def writer_process(path):
    stream = JSONLStream("test_stream", path)
    async def do():
        for i in range(5):
            await stream.put(DurableFunctionStep(step=i, result=i, name="test"))
            await asyncio.sleep(0.01)
        await stream.close()
    asyncio.run(do())

def reader_process(path):
    stream = JSONLStream("test_stream", path)
    read_events = []
    async def read():
        async for item in stream.iterate_blocking():
            read_events.append(item)
    asyncio.run(read())
    return read_events
async def test_process_read_write(temp_file_path):

    with ProcessPoolExecutor() as executor:
        writer_future = executor.submit(writer_process, temp_file_path.parent)
        reader_future = executor.submit(reader_process, temp_file_path.parent)
        reader_future2 = executor.submit(reader_process, temp_file_path.parent)

    writer_future.result()
    read_events = reader_future.result()
    read_events2 = reader_future2.result()

    assert len(read_events) == 5
    assert len(read_events2) == 5
    for i in range(5):
        assert read_events[i].result == i
        assert read_events2[i].result == i

async def test_next(stream):
    events = [DurableFunctionStep(step=i, result=i, name="test") for i in range(5)]
    for event in events:
        await stream.put(event)
    await stream.close()
    aiterator = stream.iterate_blocking()
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
        await asyncio.sleep(0.1)
        await stream.put(DurableFunctionStep(step=0, result=0, name="test"))
        await stream.close()

    asyncio.create_task(delayed_put())
    aiterator = stream.iterate_nonblocking()
    with pytest.raises(StopAsyncIteration):
        item = await anext(aiterator)


    await asyncio.sleep(0.2)
    item = await anext(aiterator)

    assert item.result == 0
