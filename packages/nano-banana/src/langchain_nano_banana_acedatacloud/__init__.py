"""Nano Banana by Ace Data Cloud: typed LangChain tools."""

from typing import ClassVar, Literal

from langchain_acedatacloud.tools import (
    AceRetrieveTool,
    AceServiceToolkit,
    AceSubmitTool,
    StrictInput,
)
from pydantic import BaseModel, Field


class NanoBananaInput(StrictInput):
    prompt: str = Field(min_length=1)
    model: Literal[
        "nano-banana", "nano-banana-2-lite", "nano-banana-2", "nano-banana-2.1", "nano-banana-pro"
    ] = "nano-banana-2"
    resolution: Literal["1K", "2K", "4K"] = "1K"
    count: int = Field(default=1, ge=1, le=4)


class NanoBananaGenerate(AceSubmitTool):
    name: str = "nano_banana_generate_image"
    description: str = (
        "Generate Nano Banana image through Ace Data Cloud. This submits one paid "
        "request; query its task ID until terminal."
    )
    args_schema: type[BaseModel] = NanoBananaInput
    endpoint: ClassVar[str] = "/nano-banana/images"

    def payload(self, args):
        return {**args, "action": "generate", "async": True}


class NanoBananaRetrieveTask(AceRetrieveTool):
    name: str = "nano_banana_retrieve_task"
    description: str = (
        "Retrieve an existing Nano Banana task by the same ID through Ace Data "
        "Cloud. Does not generate again."
    )
    endpoint: ClassVar[str] = "/nano-banana/tasks"


class NanoBananaToolkit(AceServiceToolkit):
    """Nano Banana by Ace Data Cloud. Generation is explicitly enabled by the app."""

    submit_tool: ClassVar[type[AceSubmitTool]] = NanoBananaGenerate
    retrieve_tool: ClassVar[type[AceRetrieveTool]] = NanoBananaRetrieveTask
