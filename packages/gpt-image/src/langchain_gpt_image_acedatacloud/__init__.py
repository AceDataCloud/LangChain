"""GPT Image by Ace Data Cloud: typed LangChain tools."""

from typing import ClassVar, Literal

from langchain_acedatacloud.tools import (
    AceRetrieveTool,
    AceServiceToolkit,
    AceSubmitTool,
    StrictInput,
)
from pydantic import BaseModel, Field


class GPTImageInput(StrictInput):
    prompt: str = Field(min_length=1)
    model: Literal[
        "gpt-image-2",
        "gpt-image-2.5-flare",
        "gpt-image-2.5-sunburst",
        "gpt-image-1.5",
        "gpt-image-1",
    ] = "gpt-image-2"
    size: str = Field(default="auto", pattern=r"^(auto|\d+x\d+)$")
    quality: Literal["auto", "high", "medium", "low"] = "auto"
    n: int = Field(default=1, ge=1, le=10)


class GPTImageGenerate(AceSubmitTool):
    name: str = "gpt_image_generate_image"
    description: str = (
        "Generate GPT Image image through Ace Data Cloud. This submits one paid "
        "request; query its task ID until terminal."
    )
    args_schema: type[BaseModel] = GPTImageInput
    endpoint: ClassVar[str] = "/openai/images/generations"


class GPTImageRetrieveTask(AceRetrieveTool):
    name: str = "gpt_image_retrieve_task"
    description: str = (
        "Retrieve an existing GPT Image task by the same ID through Ace Data Cloud. "
        "Does not generate again."
    )
    endpoint: ClassVar[str] = "/openai/tasks"


class GPTImageToolkit(AceServiceToolkit):
    """GPT Image by Ace Data Cloud. Generation is explicitly enabled by the app."""

    submit_tool: ClassVar[type[AceSubmitTool]] = GPTImageGenerate
    retrieve_tool: ClassVar[type[AceRetrieveTool]] = GPTImageRetrieveTask
