"""A named LangChain chat integration with Ace credential and endpoint defaults."""

from typing import Literal

from langchain_core.utils import secret_from_env
from langchain_openai.chat_models.base import BaseChatOpenAI
from pydantic import Field, SecretStr


class ChatAceDataCloud(BaseChatOpenAI):
    """Use Ace Data Cloud without specifying a custom OpenAI endpoint.

    Reuses the standard protocol implementation; only the Ace endpoint, credential
    environment, provider identity and billing-sensitive defaults are owned here.
    This class does not register itself in LangChain's upstream provider registry.
    """

    openai_api_key: SecretStr = Field(
        alias="api_key", default_factory=secret_from_env("ACEDATACLOUD_API_TOKEN")
    )
    openai_api_base: Literal["https://api.acedata.cloud/v1"] = Field(
        default="https://api.acedata.cloud/v1", alias="base_url"
    )
    model_name: str = Field(default="gpt-4o-mini", alias="model")
    use_responses_api: Literal[False] = False
    max_retries: int = 0
    stream_usage: bool = False
    request_timeout: float = Field(default=60, alias="timeout")

    @property
    def _llm_type(self) -> str:
        return "acedatacloud-chat"

    @property
    def lc_secrets(self) -> dict[str, str]:
        return {"openai_api_key": "ACEDATACLOUD_API_TOKEN"}

    def _get_ls_params(self, stop=None, **kwargs):
        params = super()._get_ls_params(stop=stop, **kwargs)
        params["ls_provider"] = "acedatacloud"
        return params
