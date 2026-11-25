"""Native LangChain tools for generating and retrieving ACE Music songs."""

from typing import Any, ClassVar, Literal

from langchain_acedatacloud.tools import (
    AceRetrieveTool,
    AceServiceToolkit,
    AceSubmitTool,
    StrictInput,
    task_result,
)
from pydantic import BaseModel, Field


class AceMusicInput(StrictInput):
    prompt: str = Field(
        min_length=1, max_length=20000, description="Describe the song or its musical style."
    )
    model: Literal["acemusic-v1.1", "acemusic-v1"] = "acemusic-v1.1"


class AceMusicGenerate(AceSubmitTool):
    name: str = "acemusic_generate_audio"
    description: str = (
        "Create a paid ACE Music song group. Save the task ID and query it for results."
    )
    args_schema: type[BaseModel] = AceMusicInput
    endpoint: ClassVar[str] = "/acemusic/audios"

    def payload(self, args):
        return {**args, "action": "generate", "custom": False, "async": True}


def _group_result(record: dict[str, Any], task_id: str) -> dict[str, Any]:
    # ACE Music records can omit finished_at; a playable individual track may be a preview.
    state = str(record.get("status") or record.get("state") or "").lower()
    adapted = dict(record)
    if state == "partial_failed":
        adapted["status"] = "failed"
    elif state == "succeeded":
        # The shared result parser also supports older records with only a completion timestamp.
        adapted["finished_at"] = record.get("finished_at") or True
    result = task_result(adapted, task_id)
    result["raw"] = record
    return result


class AceMusicRetrieveTask(AceRetrieveTool):
    name: str = "acemusic_retrieve_task"
    description: str = (
        "Query the original ACE Music task. A partial group is terminal and unsuccessful."
    )
    endpoint: ClassVar[str] = "/acemusic/tasks"

    def _run(self, task_id: str) -> dict[str, Any]:
        record = self.client.post(self.endpoint, {"action": "retrieve", "id": task_id})
        return _group_result(record, task_id)

    async def _arun(self, task_id: str) -> dict[str, Any]:
        record = await self.client.apost(self.endpoint, {"action": "retrieve", "id": task_id})
        return _group_result(record, task_id)


class AceMusicToolkit(AceServiceToolkit):
    """Query ACE Music tasks by default. Set include_generation to enable song creation."""

    submit_tool: ClassVar[type[AceSubmitTool]] = AceMusicGenerate
    retrieve_tool: ClassVar[type[AceRetrieveTool]] = AceMusicRetrieveTask
