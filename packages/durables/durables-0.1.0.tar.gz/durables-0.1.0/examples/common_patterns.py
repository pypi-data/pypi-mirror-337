import asyncio
import uuid
from typing import Callable
from durables.durable_functions import orchestrator_function, activity_function
from durables.persistence.jsonl import JSONLStream

@activity_function
async def add(x: int, y: int) -> int:
    return x + y

@activity_function
async def long_task() -> str:
    await asyncio.sleep(1)
    return "long"

@activity_function
async def constant() -> int:
    return 42


@orchestrator_function
async def chain():
    x = await constant()
    y = await add(x, 8)
    print("Das Ergebnis ist", y)


async def run_example(orchestrator: Callable) -> None:
    input_stream = JSONLStream(f"input_{uuid.uuid4().hex}")
    output_stream = JSONLStream(f"output_{uuid.uuid4().hex}")
    await orchestrator(uuid.uuid4().hex, input_stream, output_stream)


if __name__ == "__main__":
    asyncio.run(run_example(chain))