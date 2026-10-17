"""LangChain-native tools with one submission or one same-ID query per invocation."""

from typing import Any, ClassVar

from langchain_core.tools import BaseTool
from langchain_core.tools.base import BaseToolkit
from pydantic import BaseModel, ConfigDict, Field

from .client import AceAPIClient


class StrictInput(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TaskInput(StrictInput):
    task_id: str = Field(min_length=1, description="Existing task ID. Never submit again to poll.")


def task_result(data: dict[str, Any], task_id: str | None = None) -> dict[str, Any]:
    """Never treat a preview URL or accepted success=true as a completed task."""
    record = data.get("data") if isinstance(data.get("data"), dict) else data
    task_id = task_id or data.get("task_id") or record.get("task_id") or record.get("id")
    response = record.get("response")
    state = str(record.get("status") or record.get("state") or "").lower()
    failure = state in {"failed", "error", "cancelled", "canceled"}
    finished = record.get("finished_at") is not None
    terminal = finished or failure
    if isinstance(response, dict):
        response_state = str(response.get("status") or response.get("state") or "").lower()
        response_failed = (
            response.get("success") is False
            or bool(response.get("error"))
            or response_state in {"failed", "error", "cancelled", "canceled"}
        )
        if terminal and response_failed:
            failure = True
    if record.get("error") and terminal:
        failure = True
    urls: list[str] = []

    def collect(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {"url", "image_url", "video_url", "audio_url"} and isinstance(item, str):
                    if item.startswith("https://") and item not in urls:
                        urls.append(item)
                elif isinstance(item, (dict, list)):
                    collect(item)
        elif isinstance(value, list):
            for item in value:
                collect(item)

    if terminal and not failure:
        collect(response)
    return {
        "task_id": task_id,
        "status": "failed" if failure else ("succeeded" if terminal else "pending"),
        "terminal": terminal,
        "media_urls": urls,
        "raw": data,
        "next_step": (
            "Inspect the final result or failure; do not resubmit to poll."
            if terminal
            else "Query this same task_id later. Generation must not be repeated for polling."
        ),
    }


class AceSubmitTool(BaseTool):
    client: AceAPIClient = Field(exclude=True, repr=False)
    endpoint: ClassVar[str]
    metadata: dict[str, Any] = Field(
        default_factory=lambda: {"billable": True, "provider": "Ace Data Cloud"}
    )

    @staticmethod
    def submission_result(data: dict[str, Any]) -> dict[str, Any]:
        result = task_result(data)
        if not result["task_id"]:
            raise ValueError(
                "Generation response has no task ID; inspect Usage History before any retry."
            )
        return result

    def payload(self, args: dict[str, Any]) -> dict[str, Any]:
        return {**args, "async": True}

    def _run(self, **kwargs) -> dict[str, Any]:
        args = self.args_schema.model_validate(kwargs).model_dump(exclude_none=True)
        return self.submission_result(self.client.post(self.endpoint, self.payload(args)))

    async def _arun(self, **kwargs) -> dict[str, Any]:
        args = self.args_schema.model_validate(kwargs).model_dump(exclude_none=True)
        return self.submission_result(await self.client.apost(self.endpoint, self.payload(args)))


class AceRetrieveTool(BaseTool):
    client: AceAPIClient = Field(exclude=True, repr=False)
    args_schema: type[BaseModel] = TaskInput
    endpoint: ClassVar[str]
    metadata: dict[str, Any] = Field(
        default_factory=lambda: {"billable_generation": False, "provider": "Ace Data Cloud"}
    )

    def _run(self, task_id: str) -> dict[str, Any]:
        return task_result(
            self.client.post(self.endpoint, {"action": "retrieve", "id": task_id}), task_id
        )

    async def _arun(self, task_id: str) -> dict[str, Any]:
        result = await self.client.apost(self.endpoint, {"action": "retrieve", "id": task_id})
        return task_result(result, task_id)


class AceServiceToolkit(BaseToolkit):
    """Choose a service's two tools explicitly; queries alone are the default."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    client: AceAPIClient = Field(exclude=True, repr=False)
    include_generation: bool = False
    submit_tool: ClassVar[type[AceSubmitTool]]
    retrieve_tool: ClassVar[type[AceRetrieveTool]]

    def get_tools(self) -> list[BaseTool]:
        tools: list[BaseTool] = []
        if self.include_generation:
            tools.append(self.submit_tool(client=self.client))
        tools.append(self.retrieve_tool(client=self.client))
        return tools
