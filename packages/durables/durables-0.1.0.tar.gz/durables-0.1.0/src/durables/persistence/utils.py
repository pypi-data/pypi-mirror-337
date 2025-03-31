import base64
from typing import Any

import dill
from durables.models import DurableFunctionStep, DurableFunctionMessage, DurableFunctionInputRequest, DurableFunctionsPersistableRoot, DurableFunctionsPersistables


def custom_serializer(obj: DurableFunctionsPersistables) -> dict[str, Any]:
    dict_obj = obj.model_dump()
    if isinstance(obj, DurableFunctionStep):
        dict_obj["result_preview"] = str(obj.result)
        dict_obj["result"] = base64.b64encode(dill.dumps(obj.result)).decode('utf-8')
        dict_obj["id"] = str(obj.id)
    elif isinstance(obj, DurableFunctionMessage):
        dict_obj["id"] = str(obj.id)
        dict_obj["payload_preview"] = obj.payload.decode('utf-8')
        dict_obj["payload"] = base64.b64encode(obj.payload).decode('utf-8')
    elif isinstance(obj, DurableFunctionInputRequest):
        dict_obj["id"] = str(obj.id)
        # Metadata is already JSON serializable, so no special handling needed
    return dict_obj

def custom_loader(obj: dict[str, Any]) -> DurableFunctionsPersistables:
    if "result_preview" in obj:
        del obj["result_preview"]
    if "result" in obj:
        obj["result"] = dill.loads(base64.b64decode(obj["result"].encode('utf-8')))
    if "payload_preview" in obj:
        del obj["payload_preview"]
    if "payload" in obj:
        obj["payload"] = base64.b64decode(obj["payload"].encode('utf-8'))
    return DurableFunctionsPersistableRoot.model_validate(obj).root

