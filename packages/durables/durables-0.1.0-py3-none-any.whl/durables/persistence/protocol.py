from typing import Any, Iterator, Protocol
from typing import Any, Protocol, TypeVar, AsyncIterator

from durables.models import DurableFunctionsPersistables


T = TypeVar('T')

class StreamViewProtocol(Protocol, AsyncIterator[DurableFunctionsPersistables]):
    async def put(self, element: DurableFunctionsPersistables) -> None:
        """
        Inserts a new element into the stream.
        """
        ...

    async def close(self) -> None:
        """
        Closes the stream.
        """
        ...

class ReplayableStreamProtocol(Protocol):
    def iterate_blocking(self) -> StreamViewProtocol:
        """
        Returns an iterator that blocks until new data is available.
        """
        ...

    def iterate_nonblocking(self) -> StreamViewProtocol:
        """
        Returns an iterator that does not block.
        """
        ...

    async def put(self, element: DurableFunctionsPersistables) -> None:
        """
        Inserts a new element into the stream.
        """
        ...

    async def close(self) -> None:
        """
        Closes the stream.
        """
        ...


