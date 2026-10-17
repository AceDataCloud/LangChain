"""HappyHorse by Ace Data Cloud: typed LangChain tools."""

from typing import ClassVar, Literal

from langchain_acedatacloud.tools import (
    AceRetrieveTool,
    AceServiceToolkit,
    AceSubmitTool,
    StrictInput,
)
from pydantic import BaseModel, Field


class HappyHorseInput(StrictInput):
    prompt: str = Field(min_length=1)
    model: Literal["happyhorse-1.1-t2v", "happyhorse-1.0-t2v"] = "happyhorse-1.1-t2v"
    duration: int = Field(default=5, ge=3, le=15)
    resolution: Literal["720P", "1080P"] = "720P"
    ratio: Literal["16:9", "9:16", "1:1", "4:3", "3:4"] = "16:9"


class HappyHorseGenerate(AceSubmitTool):
    name: str = "happyhorse_generate_video"
    description: str = (
        "Generate HappyHorse video through Ace Data Cloud. This submits one paid "
        "request; query its task ID until terminal."
    )
    args_schema: type[BaseModel] = HappyHorseInput
    endpoint: ClassVar[str] = "/happyhorse/videos"

    def payload(self, args):
        return {**args, "action": "generate", "async": True}


class HappyHorseRetrieveTask(AceRetrieveTool):
    name: str = "happyhorse_retrieve_task"
    description: str = (
        "Retrieve an existing HappyHorse task by the same ID through Ace Data "
        "Cloud. Does not generate again."
    )
    endpoint: ClassVar[str] = "/happyhorse/tasks"


class HappyHorseToolkit(AceServiceToolkit):
    """HappyHorse by Ace Data Cloud. Generation is explicitly enabled by the app."""

    submit_tool: ClassVar[type[AceSubmitTool]] = HappyHorseGenerate
    retrieve_tool: ClassVar[type[AceRetrieveTool]] = HappyHorseRetrieveTask
