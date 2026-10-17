"""Suno by Ace Data Cloud: typed LangChain tools."""

from typing import ClassVar, Literal

from langchain_acedatacloud.tools import (
    AceRetrieveTool,
    AceServiceToolkit,
    AceSubmitTool,
    StrictInput,
)
from pydantic import BaseModel, Field


class SunoInput(StrictInput):
    prompt: str = Field(min_length=1, description="Describe the music to generate.")
    model: Literal["chirp-v6", "chirp-v6-wild", "chirp-v6-mini", "chirp-v5-5", "chirp-v5"] = (
        "chirp-v6"
    )
    instrumental: bool = True
    duration: int | None = Field(default=None, ge=10, le=360)


class SunoGenerate(AceSubmitTool):
    name: str = "suno_generate_audio"
    description: str = (
        "Generate Suno music through Ace Data Cloud. This submits one paid request; "
        "query its task ID until terminal."
    )
    args_schema: type[BaseModel] = SunoInput
    endpoint: ClassVar[str] = "/suno/audios"

    def payload(self, args):
        return {**args, "action": "generate", "custom": False, "async": True}


class SunoRetrieveTask(AceRetrieveTool):
    name: str = "suno_retrieve_task"
    description: str = (
        "Retrieve an existing Suno task by the same ID through Ace Data Cloud. Does "
        "not generate again."
    )
    endpoint: ClassVar[str] = "/suno/tasks"


class SunoToolkit(AceServiceToolkit):
    """Suno by Ace Data Cloud. Generation is explicitly enabled by the app."""

    submit_tool: ClassVar[type[AceSubmitTool]] = SunoGenerate
    retrieve_tool: ClassVar[type[AceRetrieveTool]] = SunoRetrieveTask
