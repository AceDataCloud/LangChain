"""Seedance by Ace Data Cloud: typed LangChain tools."""

from typing import ClassVar, Literal

from langchain_acedatacloud.tools import (
    AceRetrieveTool,
    AceServiceToolkit,
    AceSubmitTool,
    StrictInput,
)
from pydantic import BaseModel, Field


class SeedanceInput(StrictInput):
    prompt: str = Field(min_length=1, max_length=1000)
    model: Literal[
        "doubao-seedance-2-0-fast-260128",
        "doubao-seedance-2-0-260128",
        "doubao-seedance-2-5-260628",
    ] = "doubao-seedance-2-0-fast-260128"
    duration: int = Field(default=5, ge=1, le=30)
    resolution: Literal["480p", "720p", "1080p", "4k"] = "720p"
    ratio: Literal["16:9", "9:16", "1:1", "4:3", "3:4", "21:9", "adaptive"] = "16:9"


class SeedanceGenerate(AceSubmitTool):
    name: str = "seedance_generate_video"
    description: str = (
        "Generate Seedance video through Ace Data Cloud. This submits one paid "
        "request; query its task ID until terminal."
    )
    args_schema: type[BaseModel] = SeedanceInput
    endpoint: ClassVar[str] = "/seedance/videos"

    def payload(self, args):
        args = dict(args)
        prompt = args.pop("prompt")
        return {**args, "content": [{"type": "text", "text": prompt}], "async": True}


class SeedanceRetrieveTask(AceRetrieveTool):
    name: str = "seedance_retrieve_task"
    description: str = (
        "Retrieve an existing Seedance task by the same ID through Ace Data Cloud. "
        "Does not generate again."
    )
    endpoint: ClassVar[str] = "/seedance/tasks"


class SeedanceToolkit(AceServiceToolkit):
    """Seedance by Ace Data Cloud. Generation is explicitly enabled by the app."""

    submit_tool: ClassVar[type[AceSubmitTool]] = SeedanceGenerate
    retrieve_tool: ClassVar[type[AceRetrieveTool]] = SeedanceRetrieveTask
