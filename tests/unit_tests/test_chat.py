import asyncio
import json

import httpx
import pytest
from langchain_acedatacloud import ChatAceDataCloud
from langchain_core.messages import HumanMessage


def response(content="Hello"):
    return {
        "id": "chatcmpl-mock",
        "object": "chat.completion",
        "created": 1,
        "model": "gpt-4o-mini",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 5, "completion_tokens": 2, "total_tokens": 7},
    }


def test_named_provider_defaults_and_no_openai_key_leak(monkeypatch):
    monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "ace-secret")
    monkeypatch.setenv("OPENAI_API_KEY", "wrong-secret")
    calls = []

    def handler(request):
        calls.append(request)
        assert str(request.url) == "https://api.acedata.cloud/v1/chat/completions"
        assert request.headers["authorization"] == "Bearer ace-secret"
        return httpx.Response(200, json=response())

    model = ChatAceDataCloud(http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    reply = model.invoke("hello")
    assert reply.content == "Hello" and reply.usage_metadata["total_tokens"] == 7
    assert model._llm_type == "acedatacloud-chat"
    assert model._get_ls_params()["ls_provider"] == "acedatacloud"
    assert model.max_retries == 0 and model.use_responses_api is False
    assert "ace-secret" not in repr(model)
    assert len(calls) == 1


def test_async_and_tools_binding(monkeypatch):
    monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "ace-secret")
    calls = []

    def handler(request):
        body = json.loads(request.content)
        calls.append(body)
        return httpx.Response(200, json=response())

    model = ChatAceDataCloud(
        http_async_client=httpx.AsyncClient(transport=httpx.MockTransport(handler))
    )
    bound = model.bind_tools(
        [
            {
                "type": "function",
                "function": {
                    "name": "add",
                    "description": "Add integers",
                    "parameters": {
                        "type": "object",
                        "properties": {"a": {"type": "integer"}},
                        "required": ["a"],
                    },
                },
            }
        ]
    )
    result = asyncio.run(bound.ainvoke([HumanMessage(content="hello")]))
    assert result.content == "Hello" and calls[0]["tools"][0]["function"]["name"] == "add"


def test_missing_ace_key_does_not_fall_back_to_openai(monkeypatch):
    monkeypatch.delenv("ACEDATACLOUD_API_TOKEN", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "wrong-secret")
    with pytest.raises(ValueError):
        ChatAceDataCloud()


def test_secret_stays_out_of_langchain_serialization():
    from langchain_core.load import dumpd

    model = ChatAceDataCloud(api_key="should-never-appear")
    assert "should-never-appear" not in str(dumpd(model))
