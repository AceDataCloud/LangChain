import httpx
import pytest
from langchain_acedatacloud import AceAPIClient
from langchain_core.tools import BaseTool
from langchain_serp_acedatacloud import GoogleSearchInput, SerpToolkit
from pydantic import ValidationError


def test_invalid_search_scope_is_rejected():
    with pytest.raises(ValidationError):
        GoogleSearchInput(query="   ")
    with pytest.raises(ValidationError):
        GoogleSearchInput(query="docs", number=101)
    with pytest.raises(ValidationError):
        GoogleSearchInput(query="docs", page=0)


@pytest.mark.asyncio
async def test_sync_and_async_search_use_one_declared_request_and_keep_sources():
    import json

    seen = []
    result = {
        "organic": [
            {"title": "Reference", "link": "https://example.org/ref", "snippet": "Example"}
        ],
        "cost": {"amount": 0.01, "currency": "credit"},
    }

    def reply(request):
        assert request.method == "POST"
        assert str(request.url) == "https://api.acedata.cloud/serp/google"
        assert request.headers["authorization"] == "Bearer fixture-key"
        seen.append(json.loads(request.content))
        return httpx.Response(200, json=result)

    transport = httpx.MockTransport(reply)
    with httpx.Client(transport=transport) as sync:
        async with httpx.AsyncClient(transport=transport) as asynchronous:
            client = AceAPIClient("fixture-key", http_client=sync, http_async_client=asynchronous)
            (tool,) = SerpToolkit(client=client).get_tools()
            assert isinstance(tool, BaseTool) and tool.name == "serp_google_search"
            assert "client" not in tool.args and not seen
            assert tool.invoke({"query": "docs"}) == result
            assert (
                await tool.ainvoke({"query": "docs", "number": 2, "page": 2, "language": "en"})
                == result
            )
    assert seen == [
        {"query": "docs", "type": "search", "number": 10, "page": 1},
        {"query": "docs", "type": "search", "number": 2, "page": 2, "language": "en"},
    ]
