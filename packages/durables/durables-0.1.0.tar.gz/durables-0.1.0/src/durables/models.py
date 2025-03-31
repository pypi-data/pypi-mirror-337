from typing import Annotated, Any, Dict, Literal, Optional, TypeAlias
import uuid
from pydantic import BaseModel, Field, RootModel, model_validator


class OrchestratorSettings(BaseModel):
    wait_for_input: bool = False
    publish_input_requests: bool = False
    num_retries:int = 5



class DurableFunctionStep(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    step: int
    result: Any
    kind: Literal["activity"] = "activity"


class DurableFunctionMessage(BaseModel):
    id: int
    payload: bytes
    kind: Literal["message"] = "message"


class DurableFunctionEOS(BaseModel):
    kind: Literal["end_of_stream"] = "end_of_stream"


class DurableFunctionInputRequest(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    request_id: int
    metadata: Dict[str, Any] | None = None
    kind: Literal["input_request"] = "input_request"


DurableFunctionsPersistables = Annotated[
    DurableFunctionStep | DurableFunctionMessage | DurableFunctionEOS | DurableFunctionInputRequest,
    Field(discriminator="kind")
]

DurableFunctionsPersistableRoot = RootModel[DurableFunctionsPersistables]
