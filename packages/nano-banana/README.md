# Nano Banana by Ace Data Cloud for LangChain

![nano-banana integration icon](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2703b3ee5cdc293751a15189ed24a0eb94dc3f43/_assets/icon.jpg)

Install `langchain-nano-banana-acedatacloud` to give a LangChain application typed **Nano Banana by Ace Data Cloud** tools. This is an Ace-provided integration, not an official client of the service brand. It does not install the other four service modules. [中文](readme/README_zh_Hans.md) · [Privacy](https://github.com/AceDataCloud/LangChain/blob/main/PRIVACY.md).

## 1. Install

Install [PyPI `langchain-nano-banana-acedatacloud==0.1.0`](https://pypi.org/project/langchain-nano-banana-acedatacloud/0.1.0/). Stable wheel and source archive are public. Official LangChain [listing PR#6828](https://github.com/langchain-ai/docs/pull/6828) is merged and the [public tools directory](https://docs.langchain.com/oss/python/integrations/tools) lists this Toolkit. Fresh ordinary pip installation and query-tool loading are [verified](https://github.com/AceDataCloud/LangChain/actions/runs/39321983859).

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install langchain-nano-banana-acedatacloud==0.1.0
```

For source installation: `git clone --branch main https://github.com/AceDataCloud/LangChain.git`, `cd LangChain`, then `pip install -e packages/core -e packages/nano-banana`.

## Get the application API Key

1. [Register or sign in → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_nano_banana_api_key). If no **General application** exists, choose **Initialize General Application**.
2. Open the General application. Copy its **API Key**, or choose **Manage Keys → Create** to make a separately named LangChain key. Review expiration, usage limitations and **Allowed APIs**. Allow both the generation and same-ID task query paths used below. Confirm service access, balance and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_nano_banana_pricing). No trial allowance is promised.
3. Copy the raw token only, without `Bearer `, quotation marks or redacted characters. A `platform-...` account-management token cannot replace this application key.

![Copy the redacted application API Key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

The credential name `Dify tutorial` in the historical create-key image is illustrative; name the actual key `LangChain Nano Banana`. These are real Ace console screenshots reused from [SunoDify](https://github.com/AceDataCloud/SunoDify/tree/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial), retrieved 2026-10-18; later console layouts may differ. They show credential setup, not a LangChain GUI. Real tokens are redacted.

```bash
export ACEDATACLOUD_API_TOKEN='your application key'
```

PowerShell: `$env:ACEDATACLOUD_API_TOKEN='your application key'`. Keep the token in the environment or secret manager, never in a prompt or workflow export.

## 2. Put the key in the client, not in model arguments

```python
from langchain_acedatacloud import AceAPIClient
from langchain_nano_banana_acedatacloud import NanoBananaToolkit

# No network requests: instantiate tools and inspect their names/schemas.
kit = NanoBananaToolkit(client=AceAPIClient())
tools = kit.get_tools()  # Query-only by default.
print([tool.name for tool in tools])
```

There is no service-provider selection GUI in this package. Supply these LangChain `BaseTool` objects to your application or agent. Screenshots of another host's plugin authorization are not instructions for this Python integration.

## 3. First use, then query the same ID

After reviewing [current service prices](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_nano_banana_pricing) and deliberately authorizing one generation:

```python
kit = NanoBananaToolkit(client=AceAPIClient(), include_generation=True)
generate, retrieve = kit.get_tools()
# This line submits one paid generation if you choose to run it:
submitted = generate.invoke({"prompt": "A minimal watercolor sunrise over a lake."})
task_id = submitted["task_id"]
# Query the original ID; never call generate again just to wait:
result = retrieve.invoke({"task_id": task_id})
print(result["status"], result["terminal"], result["media_urls"])
```

`nano_banana_generate_image` submits one asynchronous request to `/nano-banana/images`. `nano_banana_retrieve_task` calls `/nano-banana/tasks` with `action=retrieve` and the original `id`. A pending result is normal. Query that ID later until `terminal=true`; then inspect success/failure and final media URLs. The example shape is illustrative, not an actual paid result. Advanced edit/extend actions are not exposed in this initial toolkit.

## Troubleshooting and cost

401: raw Key or token environment; 403: permissions, balance, expiry, Allowed APIs and response details; 429: reduce concurrency. For pending or a timeout, inspect the same task before any new submission. No automatic retries or hidden polling are performed. [Usage History](https://platform.acedata.cloud/console/usages?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_nano_banana_usage) owns actual Credits. Avoid printing credentials or sending them to a model.
