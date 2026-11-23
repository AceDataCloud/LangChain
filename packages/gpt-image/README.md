# GPT Image by Ace Data Cloud for LangChain

![gpt-image integration icon](https://raw.githubusercontent.com/AceDataCloud/GPTImageDify/910a7d746581a42dab5fe88c16b3134a44b2db1b/_assets/icon.png)

Install `langchain-gpt-image-acedatacloud` to give a LangChain application typed **GPT Image by Ace Data Cloud** tools. This is an Ace-provided integration, not an official client of the service brand. It does not install the other four service modules. [中文](readme/README_zh_Hans.md) · [Privacy](https://github.com/AceDataCloud/LangChain/blob/main/PRIVACY.md).

## 1. Install

Install [PyPI `langchain-gpt-image-acedatacloud==0.1.1`](https://pypi.org/project/langchain-gpt-image-acedatacloud/0.1.1/). Official LangChain [listing PR#6836](https://github.com/langchain-ai/docs/pull/6836) is merged and the [public tools directory](https://docs.langchain.com/oss/python/integrations/tools) lists this Toolkit. The shared core dependency stays at 0.1.0; the other service packages are independently versioned.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install langchain-gpt-image-acedatacloud==0.1.1
```

For source installation: `git clone --branch main https://github.com/AceDataCloud/LangChain.git`, `cd LangChain`, then `pip install -e packages/core -e packages/gpt-image`.

## Get the application API Key

1. [Register or sign in → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_gpt_image_api_key). If no **General application** exists, choose **Initialize General Application**.
2. Open the General application. Copy its **API Key**, or choose **Manage Keys → Create** to make a separately named LangChain key. Review expiration, usage limitations and **Allowed APIs**. Allow both the generation and same-ID task query paths used below. Confirm service access, balance and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_gpt_image_pricing). No trial allowance is promised.
3. Copy the raw token only, without `Bearer `, quotation marks or redacted characters. A `platform-...` account-management token cannot replace this application key.

![Copy the redacted application API Key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

The credential name `Dify tutorial` in the historical create-key image is illustrative; name the actual key `LangChain GPT Image`. These are real Ace console screenshots reused from [SunoDify](https://github.com/AceDataCloud/SunoDify/tree/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial), retrieved 2026-10-18; later console layouts may differ. They show credential setup, not a LangChain GUI. Real tokens are redacted.

```bash
export ACEDATACLOUD_API_TOKEN='your application key'
```

PowerShell: `$env:ACEDATACLOUD_API_TOKEN='your application key'`. Keep the token in the environment or secret manager, never in a prompt or workflow export.

## 2. Put the key in the client, not in model arguments

```python
from langchain_acedatacloud import AceAPIClient
from langchain_gpt_image_acedatacloud import GPTImageToolkit

# No network requests: instantiate tools and inspect their names/schemas.
kit = GPTImageToolkit(client=AceAPIClient())
tools = kit.get_tools()  # Query-only by default.
print([tool.name for tool in tools])
```

There is no service-provider selection GUI in this package. Supply these LangChain `BaseTool` objects to your application or agent. Screenshots of another host's plugin authorization are not instructions for this Python integration.

## 3. First use, then query the same ID

After reviewing [current service prices](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_gpt_image_pricing) and deliberately authorizing one generation:

```python
kit = GPTImageToolkit(client=AceAPIClient(), include_generation=True)
generate, retrieve = kit.get_tools()
# This line submits one paid generation if you choose to run it:
submitted = generate.invoke({"prompt": "A minimal watercolor sunrise over a lake."})
task_id = submitted["task_id"]
# Query the original ID; never call generate again just to wait:
result = retrieve.invoke({"task_id": task_id})
print(result["status"], result["terminal"], result["media_urls"])
```

`gpt_image_generate_image` submits one asynchronous request to `/openai/images/generations`. `gpt_image_retrieve_task` calls `/openai/tasks` with `action=retrieve` and the original `id`. A pending result is normal. Query that ID later until `terminal=true`; then inspect success/failure and final media URLs. The example shape is illustrative, not an actual paid result. Advanced edit/extend actions are not exposed in this initial toolkit.

## Model and parameter coverage

Version 0.1.1 accepts all 24 model IDs and eight quality values in the reviewed [public generation API](https://platform.acedata.cloud/api/v1/apis/8f01fe72-8a3e-4872-8d8d-330cde179b3a/), including DALL-E 2/3, GPT Image 2.6 variants and Nano Banana 2.1. Quality choices remain model-specific: DALL-E 2 accepts `standard`; DALL-E 3 accepts `standard` or `hd` and requires `n=1`. Unsupported explicit DALL-E values fail before submission.

For the five models already supported in 0.1.0 (`gpt-image-1`, `gpt-image-1.5`, `gpt-image-2`, `gpt-image-2.5-flare`, `gpt-image-2.5-sunburst`), absent `quality` and `size` retain the existing `auto` defaults. New models omit both fields unless supplied. Explicit `None` omits either field even for an older model. `size="auto"` requests prompt-based canvas selection; an omitted size uses the model's default canvas. Explicit supported values pass through unchanged. This package exposes generation and task lookup; image editing and GIF-specific parameters are not exposed.

The checked-in `contracts/gpt-image.json` owns the typed enum snapshot. Maintainers can explicitly refresh it with `python scripts/sync_gpt_image_contract.py --refresh`, review the diff, and run `--check` offline. Refreshing reads documentation and never generates an image.

## Troubleshooting and cost

401: raw Key or token environment; 403: permissions, balance, expiry, Allowed APIs and response details; 429: reduce concurrency. For pending or a timeout, inspect the same task before any new submission. No automatic retries or hidden polling are performed. [Usage History](https://platform.acedata.cloud/console/usages?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_gpt_image_usage) owns actual Credits. Avoid printing credentials or sending them to a model.
