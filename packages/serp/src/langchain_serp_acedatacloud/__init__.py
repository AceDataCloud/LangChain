"""LangChain Google Search tools for the Ace Data Cloud Serp API."""

from typing import Any

from langchain_acedatacloud import AceAPIClient
from langchain_acedatacloud.tools import StrictInput
from langchain_core.tools import BaseTool, BaseToolkit
from pydantic import BaseModel, Field


class GoogleSearchInput(StrictInput):
    query: str = Field(
        min_length=1, max_length=2048, pattern=r"\S", description="Web search query."
    )
    number: int = Field(default=10, ge=1, le=100, description="Number of results to request.")
    page: int = Field(default=1, ge=1, le=100, description="Results page, starting at one.")
    country: str | None = Field(default=None, description="Optional country filter, such as US.")
    language: str | None = Field(default=None, description="Optional language code, such as en.")


class AceGoogleSearch(BaseTool):
    """Return the provider's source links, snippets, and any reported usage."""

    name: str = "serp_google_search"
    description: str = (
        "Search Google through Ace Data Cloud and return web results with source URLs. "
        "Each call uses search credits."
    )
    args_schema: type[BaseModel] = GoogleSearchInput
    client: AceAPIClient = Field(exclude=True, repr=False)

    @staticmethod
    def _payload(query: str, number: int, page: int, country: str | None, language: str | None):
        inputs = GoogleSearchInput(
            query=query, number=number, page=page, country=country, language=language
        )
        return {"type": "search", **inputs.model_dump(exclude_none=True)}

    def _run(
        self,
        query: str,
        number: int = 10,
        page: int = 1,
        country: str | None = None,
        language: str | None = None,
    ) -> dict[str, Any]:
        return self.client.post(
            "/serp/google", self._payload(query, number, page, country, language)
        )

    async def _arun(
        self,
        query: str,
        number: int = 10,
        page: int = 1,
        country: str | None = None,
        language: str | None = None,
    ) -> dict[str, Any]:
        return await self.client.apost(
            "/serp/google", self._payload(query, number, page, country, language)
        )


class SerpToolkit(BaseToolkit):
    """Provide Google web search with a separately configured Ace Data Cloud client."""

    client: AceAPIClient = Field(default_factory=AceAPIClient, exclude=True, repr=False)
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> list[BaseTool]:
        return [AceGoogleSearch(client=self.client)]
