import json
import subprocess
import sys
from pathlib import Path
from typing import get_args

import httpx
import pytest
from langchain_acedatacloud import AceAPIClient
from langchain_gpt_image_acedatacloud import GPTImageInput, GPTImageToolkit
from langchain_gpt_image_acedatacloud._contract import ImageModel, ImageQuality
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = json.loads((ROOT / "contracts/gpt-image.json").read_text())


def test_generated_types_match_the_complete_reviewed_public_contract():
    subprocess.run(
        [sys.executable, "scripts/sync_gpt_image_contract.py", "--check"],
        cwd=ROOT,
        check=True,
    )
    assert list(get_args(ImageModel)) == CONTRACT["fields"]["model"]["enum"]
    assert list(get_args(ImageQuality)) == CONTRACT["fields"]["quality"]["enum"]
    assert len(get_args(ImageModel)) == 24
    assert len(get_args(ImageQuality)) == 8


def test_all_image_models_reach_one_request_with_compatible_defaults():
    calls = []

    def handler(request):
        calls.append(json.loads(request.content))
        assert request.url.path == CONTRACT["path"]
        return httpx.Response(200, json={"task_id": "offline-task"})

    transport = httpx.MockTransport(handler)
    client = AceAPIClient(
        "offline-placeholder",
        http_client=httpx.Client(transport=transport),
        http_async_client=httpx.AsyncClient(transport=transport),
    )
    tool = GPTImageToolkit(client=client, include_generation=True).get_tools()[0]
    for model in get_args(ImageModel):
        result = tool.invoke({"prompt": "Offline fixture", "model": model})
        assert result["task_id"] == "offline-task"
    assert [body["model"] for body in calls] == list(get_args(ImageModel))
    legacy = {
        "gpt-image-2",
        "gpt-image-2.5-flare",
        "gpt-image-2.5-sunburst",
        "gpt-image-1.5",
        "gpt-image-1",
    }
    for body in calls:
        if body["model"] in legacy:
            assert body["quality"] == body["size"] == "auto"
        else:
            assert "quality" not in body and "size" not in body
    assert all(body["n"] == 1 and body["async"] is True for body in calls)


@pytest.mark.parametrize("model", ["dall-e-2", "dall-e-3"])
@pytest.mark.parametrize("quality", ["auto", "low"])
def test_dall_e_rejects_unsupported_explicit_quality(model, quality):
    with pytest.raises(ValidationError, match="quality"):
        GPTImageInput(prompt="Offline fixture", model=model, quality=quality)


def test_explicit_existing_values_are_preserved_and_dall_e_count_is_validated():
    value = GPTImageInput(
        prompt="Offline fixture", model="gpt-image-2", quality="low", size="1024x1024"
    )
    assert value.model_dump(exclude_none=True)["quality"] == "low"
    assert value.model_dump(exclude_none=True)["size"] == "1024x1024"
    with pytest.raises(ValidationError, match="n=1"):
        GPTImageInput(prompt="Offline fixture", model="dall-e-3", n=2)


def test_explicit_none_uses_api_default_even_for_legacy_models():
    value = GPTImageInput(prompt="Offline fixture", quality=None, size=None)
    assert "quality" not in value.model_dump(exclude_none=True)
    assert "size" not in value.model_dump(exclude_none=True)


@pytest.mark.parametrize("model,size", [("dall-e-2", "auto"), ("dall-e-3", "256x256")])
def test_dall_e_rejects_unsupported_explicit_size(model, size):
    with pytest.raises(ValidationError, match="size"):
        GPTImageInput(prompt="Offline fixture", model=model, size=size)
