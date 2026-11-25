"""GPT Image by Ace Data Cloud: typed LangChain tools."""

from typing import ClassVar

from langchain_acedatacloud.tools import (
    AceRetrieveTool,
    AceServiceToolkit,
    AceSubmitTool,
    StrictInput,
)
from pydantic import BaseModel, Field, model_validator

from ._contract import ImageModel, ImageQuality

# Keep the five models supported by 0.1.0 byte-compatible when arguments are absent.
_LEGACY_DEFAULT_MODELS = {
    "gpt-image-2",
    "gpt-image-2.5-flare",
    "gpt-image-2.5-sunburst",
    "gpt-image-1.5",
    "gpt-image-1",
}


class GPTImageInput(StrictInput):
    prompt: str = Field(min_length=1)
    model: ImageModel = "gpt-image-2"
    size: str | None = Field(default=None, pattern=r"^(auto|\d+x\d+)$")
    quality: ImageQuality | None = None
    n: int = Field(default=1, ge=1, le=10)

    @model_validator(mode="after")
    def validate_model_parameters(self):
        if self.model in _LEGACY_DEFAULT_MODELS:
            if "size" not in self.model_fields_set:
                self.size = "auto"
            if "quality" not in self.model_fields_set:
                self.quality = "auto"
        if self.model == "dall-e-2" and self.quality not in {None, "standard"}:
            raise ValueError("DALL-E 2 quality must be standard or omitted")
        if self.model == "dall-e-2" and self.size not in {None, "256x256", "512x512", "1024x1024"}:
            raise ValueError("DALL-E 2 size must be 256x256, 512x512, 1024x1024 or omitted")
        if self.model == "dall-e-3":
            if self.quality not in {None, "standard", "hd"}:
                raise ValueError("DALL-E 3 quality must be standard, hd or omitted")
            if self.size not in {None, "1024x1024", "1792x1024", "1024x1792"}:
                raise ValueError("DALL-E 3 size must be 1024x1024, 1792x1024, 1024x1792 or omitted")
            if self.n != 1:
                raise ValueError("DALL-E 3 requires n=1")
        return self


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
