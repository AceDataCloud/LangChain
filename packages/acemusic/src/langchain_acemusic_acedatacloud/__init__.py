"""Native LangChain tools for generating and retrieving ACE Music songs."""

from typing import Any, ClassVar, Literal

from langchain_acedatacloud.tools import (
    AceRetrieveTool,
    AceServiceToolkit,
    AceSubmitTool,
    StrictInput,
    task_result,
)
from pydantic import BaseModel, Field, model_validator

AssetType = Literal["midi", "image", "video"]


class AceMusicInput(StrictInput):
    prompt: str = Field(
        min_length=1, max_length=20000, description="Describe the song or its musical style."
    )
    model: Literal["acemusic-v1.1", "acemusic-v1"] = "acemusic-v1.1"
    asset_id: str | None = Field(default=None, min_length=1, max_length=128)
    asset_type: AssetType | None = None

    @model_validator(mode="after")
    def check_reference(self):
        if (self.asset_id is None) != (self.asset_type is None):
            raise ValueError("Provide both asset ID and asset type")
        if self.asset_id and self.model != "acemusic-v1.1":
            raise ValueError("Reference assets require acemusic-v1.1")
        return self


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


class AssetUploadInput(StrictInput):
    type: AssetType
    url: str = Field(pattern=r"^https://", min_length=9)
    name: str | None = Field(default=None, min_length=1)


class AceMusicUploadAsset(AceSubmitTool):
    name: str = "acemusic_upload_asset"
    description: str = (
        "Import a MIDI, image or video asset for a separate charge. Save the original task ID."
    )
    args_schema: type[BaseModel] = AssetUploadInput
    endpoint: ClassVar[str] = "/acemusic/assets"

    def payload(self, args):
        return {**args, "action": "upload", "async": True}


class AssetQueryInput(StrictInput):
    id: str | None = Field(default=None, min_length=1, max_length=128)
    type: AssetType | None = None
    page: int | None = Field(default=None, ge=1, le=10001)
    page_size: int | None = Field(default=None, ge=1, le=100)

    @model_validator(mode="after")
    def check_shape(self):
        if self.id and any(v is not None for v in (self.type, self.page, self.page_size)):
            raise ValueError("Use an asset ID or pagination and an optional type filter")
        return self


class AceMusicRetrieveAssets(AceRetrieveTool):
    name: str = "acemusic_retrieve_assets"
    description: str = "Read an owned asset by ID, or omit ID for a free page of owned assets."
    args_schema: type[BaseModel] = AssetQueryInput
    endpoint: ClassVar[str] = "/acemusic/assets"

    def payload(self, args):
        return {
            "action": "retrieve",
            **AssetQueryInput.model_validate(args).model_dump(exclude_none=True),
        }

    def _run(self, **kwargs):
        return self.client.post(self.endpoint, self.payload(kwargs))

    async def _arun(self, **kwargs):
        return await self.client.apost(self.endpoint, self.payload(kwargs))


class AceMusicToolkit(AceServiceToolkit):
    """Query ACE Music tasks by default. Set include_generation to enable song creation."""

    submit_tool: ClassVar[type[AceSubmitTool]] = AceMusicGenerate
    retrieve_tool: ClassVar[type[AceRetrieveTool]] = AceMusicRetrieveTask

    include_assets: bool = False

    def get_tools(self):
        tools = super().get_tools()
        if self.include_assets:
            additions = [AceMusicRetrieveAssets(client=self.client)]
            if self.include_generation:
                additions.insert(0, AceMusicUploadAsset(client=self.client))
            tools[-1:-1] = additions
        return tools
