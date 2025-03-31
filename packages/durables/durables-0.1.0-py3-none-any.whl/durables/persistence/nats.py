import asyncio
import json
import logging
import base64
import dill
from typing import Any, Optional
import uuid
from concurrent.futures import ThreadPoolExecutor

import nats
from nats.js import JetStreamContext
from nats.aio.client import Client as NATS
from nats.js.api import ConsumerConfig, RetentionPolicy, StreamConfig, DeliverPolicy, AckPolicy

from durables.persistence.utils import custom_loader, custom_serializer
from durables.models import DurableFunctionEOS, DurableFunctionsPersistables
from durables.persistence.protocol import StreamViewProtocol

logger = logging.getLogger(__name__)


class NatsStreamView(StreamViewProtocol):
    def __init__(self, parent: "NatsStream", consumer_name: str, blocking: bool = True):
        self.parent = parent
        self.blocking = blocking
        self.consumer_name = consumer_name
        self.queue: asyncio.Queue[DurableFunctionsPersistables] = asyncio.Queue()
        self.subscription: JetStreamContext.PullSubscription | None = None
        self.stopped = False
        self.task: asyncio.Task[None] | None = None
        self.init_task = asyncio.create_task(self._setup_consumer())


    def __del__(self) -> None:
        if self.init_task is not None:
            self.init_task.cancel()
        if self.task is not None:
            self.task.cancel()

    async def _setup_consumer(self) -> None:
        if self.parent.js is None:
            raise RuntimeError("JetStream context is not initialized")
        
        try:
            consumer_info = await self.parent.js.consumer_info(
                self.parent.stream_name, 
                self.consumer_name
            )
        except Exception:
            await self.parent.js.add_consumer(
                stream=self.parent.stream_name,
                config=ConsumerConfig(
                    durable_name=self.consumer_name,
                    ack_policy=AckPolicy.ALL,
                    deliver_policy=DeliverPolicy.ALL,
                    filter_subject=self.parent.subject,
                )
            )
        
        self.subscription = await self.parent.js.pull_subscribe(
            subject=self.parent.subject,
            durable=self.consumer_name,
            stream=self.parent.stream_name
        )
        
        fetching = asyncio.Event()
        self.task = asyncio.create_task(self._fetch_messages(fetching))
        await fetching.wait()

    async def _fetch_messages(self, event: asyncio.Event) -> None:
        if self.subscription is None:
            return
        timeout: float | None  = 1e-1
        while not self.stopped:
            try:
                message, = await self.subscription.fetch(timeout=timeout)

                payload = json.loads(message.data.decode())
                item = custom_loader(payload)
                
                await self.queue.put(item)
                await message.ack()

                if isinstance(item, DurableFunctionEOS):
                    self.stopped = True
                    break
            except nats.errors.TimeoutError:
                timeout = None
            event.set()

    def __aiter__(self) -> "NatsStreamView":
        return self

    async def __anext__(self) -> DurableFunctionsPersistables:        
        if not self.parent.init_task.done():
            await self.parent.init_task
        if self.subscription is None or self.task is None:
            await self.init_task
        
        if self.blocking:
            item = await self.queue.get()
        else:
            if self.queue.empty() and self.task is not None:
                self.task.cancel()
                raise StopAsyncIteration
            
            item = self.queue.get_nowait()
        
        if isinstance(item, DurableFunctionEOS):
            self.stopped = True
            raise StopAsyncIteration
        
        return item

    async def put(self, element: DurableFunctionsPersistables) -> None:
        await self.parent.put(element)

    async def close(self) -> None:
        self.stopped = True
        if self.subscription:
            await self.subscription.unsubscribe()
        await self.parent.close()


class NatsStream:
    def __init__(
        self, 
        stream_id: str, 
        nats_servers: list[str] = ["nats://localhost:4222"], 
        subject_prefix: str = "durables"
    ):
        self.stream_id = stream_id
        self.stream_name = f"DURABLE"
        self.subject = f"{subject_prefix}.{stream_id}"
        self.subject_prefix = subject_prefix
        self.nats_servers = nats_servers
        self.nc: NATS = NATS()
        self.js: JetStreamContext = self.nc.jetstream()
        self.init_task = asyncio.create_task(self.__async_init())

    def __del__(self) -> None:
        if self.init_task is not None:
            self.init_task.cancel()

    async def __async_init(self) -> None:
        await self.nc.connect(servers=self.nats_servers)
        
        try:
            await self.js.stream_info(self.stream_name)
        except Exception as e:
            await self.js.add_stream(
                StreamConfig(
                    name=self.stream_name,
                    subjects=[f"{self.subject_prefix}.>"],
                    retention=RetentionPolicy.LIMITS,
                    max_msgs=1000000,
                    max_bytes=1024 * 1024 * 1024,  # 1 GB
                    max_age=30 * 24 * 60 * 60,  # 30 days
                )
            )

    def iterate_blocking(self) -> NatsStreamView:
        """Returns an iterator that blocks until new data is available."""
        consumer_name = f"{uuid.uuid4().hex}"
        return NatsStreamView(self, consumer_name, blocking=True)

    def iterate_nonblocking(self) -> NatsStreamView:
        """Returns an iterator that does not block."""
        consumer_name = f"{uuid.uuid4().hex}"
        return NatsStreamView(self, consumer_name, blocking=False)

    async def put(self, element: DurableFunctionsPersistables) -> None:
        """Inserts a new element into the stream."""        
        if not self.init_task.done():
            await self.init_task

        payload = json.dumps(custom_serializer(element))
        await self.js.publish(subject=self.subject, payload=payload.encode())

    async def close(self) -> None:
        """Closes the stream."""
        await self.put(DurableFunctionEOS())
