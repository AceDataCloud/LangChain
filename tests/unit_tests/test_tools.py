import asyncio
import importlib
import json

import httpx
import pytest
from langchain_acedatacloud import AceAPIClient
from langchain_acedatacloud.tools import task_result
from pydantic import ValidationError

SERVICES = [
    ("suno", "Suno", "/suno/audios", "/suno/tasks"),
    ("seedance", "Seedance", "/seedance/videos", "/seedance/tasks"),
    ("happyhorse", "HappyHorse", "/happyhorse/videos", "/happyhorse/tasks"),
    ("gpt_image", "GPTImage", "/openai/images/generations", "/openai/tasks"),
    ("nano_banana", "NanoBanana", "/nano-banana/images", "/nano-banana/tasks"),
]


def toolkit(slug, cls, handler):
    module = importlib.import_module(f"langchain_{slug}_acedatacloud")
    transport = httpx.MockTransport(handler)
    client = AceAPIClient(
        "test-secret",
        http_client=httpx.Client(transport=transport),
        http_async_client=httpx.AsyncClient(transport=transport),
    )
    return getattr(module, cls + "Toolkit")(client=client, include_generation=True)


@pytest.mark.parametrize("slug,cls,endpoint,query", SERVICES)
def test_distinct_typed_service_submission_and_same_id_query(slug, cls, endpoint, query):
    calls = []

    def handler(request):
        body = json.loads(request.content)
        calls.append((request.url.path, body))
        assert request.headers["Authorization"] == "Bearer test-secret"
        if request.url.path == endpoint:
            assert body["async"] is True
            assert "api_token" not in body
            if slug == "seedance":
                assert body["content"] == [{"type": "text", "text": "sunrise"}]
                assert "prompt" not in body
            else:
                assert body["prompt"] == "sunrise"
            return httpx.Response(200, json={"task_id": "owned-task", "success": True})
        assert request.url.path == query
        assert body == {"action": "retrieve", "id": "owned-task"}
        return httpx.Response(
            200,
            json={
                "id": "owned-task",
                "finished_at": 123,
                "response": {"success": True, "data": [{"url": "https://example.org/final.mp4"}]},
            },
        )

    kit = toolkit(slug, cls, handler)
    generate, retrieve = kit.get_tools()
    assert "client" not in generate.tool_call_schema.model_json_schema()["properties"]
    submitted = generate.invoke({"prompt": "sunrise"})
    assert submitted["status"] == "pending" and submitted["terminal"] is False
    result = retrieve.invoke({"task_id": submitted["task_id"]})
    assert result["terminal"] is True
    assert result["status"] == "succeeded"
    assert result["media_urls"] == ["https://example.org/final.mp4"]
    assert len(calls) == 2
    assert "test-secret" not in repr(kit)


@pytest.mark.parametrize("slug,cls,endpoint,query", SERVICES)
def test_query_only_default_and_async(slug, cls, endpoint, query):
    seen = []

    def handler(request):
        seen.append(request.url.path)
        return httpx.Response(
            200,
            json={"id": "old", "response": {"data": [{"url": "https://example.org/preview.mp4"}]}},
        )

    kit = toolkit(slug, cls, handler)
    kit.include_generation = False
    assert len(kit.get_tools()) == 1
    retrieve = kit.get_tools()[0]
    result = asyncio.run(retrieve.ainvoke({"task_id": "old"}))
    assert result["terminal"] is False and result["media_urls"] == []
    assert seen == [query]


@pytest.mark.parametrize("status", [401, 403, 429, 500])
def test_errors_preserve_http_status_and_never_retry(status):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(status, json={"error": {"code": "example"}})

    generate = toolkit("suno", "Suno", handler).get_tools()[0]
    with pytest.raises(httpx.HTTPStatusError) as exc:
        generate.invoke({"prompt": "example"})
    assert exc.value.response.status_code == status
    assert len(calls) == 1


def test_unknown_input_cannot_override_async_or_inject_credentials():
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(200, json={})

    generate = toolkit("suno", "Suno", handler).get_tools()[0]
    for extra in [
        {"api_token": "leak"},
        {"async": False},
        {"callback_url": "https://evil.example"},
    ]:
        with pytest.raises(ValidationError):
            generate.invoke({"prompt": "example", **extra})
    assert not calls


def test_terminal_failure_and_preview_boundaries():
    assert task_result({"success": True, "task_id": "pending"})["terminal"] is False
    result = task_result(
        {"finished_at": 2, "response": {"success": False, "error": {"code": "failed"}}}
    )
    assert result["terminal"] is True and result["status"] == "failed"
    assert result["media_urls"] == []
    assert task_result({"state": "failed"})["status"] == "failed"


def test_missing_submission_id_is_not_claimed_as_pending_or_retried():
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(200, json={"success": False, "error": {"code": "upstream"}})

    generate = toolkit("suno", "Suno", handler).get_tools()[0]
    with pytest.raises(ValueError, match="inspect Usage History"):
        generate.invoke({"prompt": "example"})
    assert len(calls) == 1


def test_finished_error_without_success_flag_is_failed():
    result = task_result({"finished_at": 2, "response": {"error": {"code": "moderation"}}})
    assert result["status"] == "failed" and result["terminal"] is True
