from pathlib import Path
import json
from filelock import FileLock
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
import logging
from durables.models import DurableFunctionEOS, DurableFunctionsPersistables
from durables.persistence.utils import custom_loader, custom_serializer
logger = logging.getLogger(__name__)




class StreamView():
    def __init__(self, parent: "JSONLStream"):
        self.parent = parent
    def __aiter__(self) -> "StreamView":
        return self
    async def __anext__(self) -> DurableFunctionsPersistables:
        raise NotImplementedError
    
    async def put(self, item: DurableFunctionsPersistables) -> None:
        await self.parent.put(item)

    async def close(self) -> None:
        await self.parent.close()

class JSONLStream:
    def __init__(self, stream_id: str, file_path: Path=Path(".durable_storage")):
        self.file_path = file_path / f"{stream_id}/{stream_id}.jsonl"
        # Ensure file exists.
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.touch(exist_ok=True)

    def iterate_blocking(self) -> StreamView:
        logging.debug("Starting JSONLStream iterator")
        file_obj = open(self.file_path, "r")
        filewatch_event = asyncio.Event()
        loop = asyncio.get_running_loop()
        file_path_str = str(self.file_path)

        class ChangeHandler(FileSystemEventHandler):
            def on_modified(self, event: FileSystemEvent) -> None:
                if event.src_path == file_path_str:
                    # Schedule the event so it’s triggered in asyncio
                    logger.debug("file change detected in %s", file_path_str)
                    loop.call_soon_threadsafe(filewatch_event.set)

        event_handler = ChangeHandler()
        observer = Observer()
        observer.schedule(event_handler, str(self.file_path.parent), recursive=False)
        observer.start()

        class _StreamView(StreamView):
            def __del__(self) -> None:
                observer.stop()
                observer.join()
            async def __anext__(self) -> DurableFunctionsPersistables:
                with FileLock(f"{self.parent.file_path}.lock"):
                    line = file_obj.readline()
                while not line:
                    await filewatch_event.wait()
                    filewatch_event.clear()
                    with FileLock(f"{self.parent.file_path}.lock"):
                        line = file_obj.readline()
                item = custom_loader(json.loads(line))
                # print(item)
                if isinstance(item, DurableFunctionEOS):
                    raise StopAsyncIteration
                return item
        return _StreamView(self)
    
    def iterate_nonblocking(self) -> StreamView:
        logging.debug("Starting JSONLStream iterator")
        file_obj = open(self.file_path, "r")
        
        class _StreamView(StreamView):
            async def __anext__(self) -> DurableFunctionsPersistables:
                with FileLock(f"{self.parent.file_path}.lock"):
                    line = file_obj.readline()
                if not line:
                    raise StopAsyncIteration
                item = custom_loader(json.loads(line))
                if isinstance(item, DurableFunctionEOS):
                    raise StopAsyncIteration
                return item

        return _StreamView(self)

    async def put(self, event: DurableFunctionsPersistables) -> None:
        """Append an event to the file (and eventually to the queue)."""
        with FileLock(f"{self.file_path}.lock"):
            with open(self.file_path, "a") as f:
                json.dump(custom_serializer(event), f)
                f.write("\n")

    async def close(self) -> None:
        """Send EndOfStream marker and finalize."""
        with FileLock(f"{self.file_path}.lock"):
            with open(self.file_path, "a") as f:
                json.dump(custom_serializer(DurableFunctionEOS()), f)
                f.write("\n")