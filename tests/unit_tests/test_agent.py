"""Actual create_agent/ToolNode loop using mocked model and service transports."""

import importlib
import json

import httpx
import pytest
from langchain.agents import create_agent
from langchain_acedatacloud import AceAPIClient, ChatAceDataCloud
from langchain_core.messages import ToolMessage


@pytest.mark.parametrize(
    "slug,cls,task_path",
    [
        ("suno", "Suno", "/suno/tasks"),
        ("seedance", "Seedance", "/seedance/tasks"),
        ("happyhorse", "HappyHorse", "/happyhorse/tasks"),
        ("gpt_image", "GPTImage", "/openai/tasks"),
        ("nano_banana", "NanoBanana", "/nano-banana/tasks"),
    ],
)
def test_native_agent_executes_service_query_and_returns_tool_message(slug, cls, task_path):
    requests = []

    def handler(request):
        body = json.loads(request.content)
        requests.append((request.url.path, body))
        if request.url.path == task_path:
            assert body == {"action": "retrieve", "id": "owned-task"}
            return httpx.Response(
                200,
                json={"id": "owned-task", "finished_at": 123, "response": {"success": True}},
            )
        assert request.url.path == "/v1/chat/completions"
        message = {"role": "assistant", "content": "The existing task completed."}
        reason = "stop"
        if len(requests) == 1:
            assert len(body["tools"]) == 1
            assert body["tools"][0]["function"]["name"] == f"{slug}_retrieve_task"
            message = {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": "call_query",
                        "type": "function",
                        "function": {
                            "name": f"{slug}_retrieve_task",
                            "arguments": '{"task_id":"owned-task"}',
                        },
                    }
                ],
            }
            reason = "tool_calls"
        else:
            tool_messages = [item for item in body["messages"] if item["role"] == "tool"]
            assert len(tool_messages) == 1
            assert json.loads(tool_messages[0]["content"])["terminal"] is True
        return httpx.Response(
            200,
            json={
                "id": "chatcmpl-agent",
                "object": "chat.completion",
                "created": 1,
                "model": "gpt-4o-mini",
                "choices": [{"index": 0, "message": message, "finish_reason": reason}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            },
        )

    transport = httpx.MockTransport(handler)
    model = ChatAceDataCloud(
        api_key="offline-model-key", http_client=httpx.Client(transport=transport)
    )
    client = AceAPIClient("offline-tool-key", http_client=httpx.Client(transport=transport))
    module = importlib.import_module(f"langchain_{slug}_acedatacloud")
    tools = getattr(module, cls + "Toolkit")(client=client).get_tools()
    agent = create_agent(model, tools)
    result = agent.invoke({"messages": [{"role": "user", "content": "Query my owned-task."}]})
    assert isinstance(result["messages"][-2], ToolMessage)
    assert result["messages"][-1].content == "The existing task completed."
    assert [path for path, _ in requests] == [
        "/v1/chat/completions",
        task_path,
        "/v1/chat/completions",
    ]
