# Ace Data Cloud for LangChain

A named `ChatAceDataCloud` chat model and **five separately installable service toolkits**: Suno, Seedance, HappyHorse, GPT Image and Nano Banana **by Ace Data Cloud**. This project is maintained by Ace Data Cloud; it is not an official client of those service brands.

[简体中文](https://github.com/AceDataCloud/LangChain/blob/main/readme/README_zh_Hans.md) · [Privacy](https://github.com/AceDataCloud/LangChain/blob/main/PRIVACY.md) · [Source](https://github.com/AceDataCloud/LangChain)

**Stable release preparation:** the native integration source is merged on `main`. Version `0.1.0` is being prepared for all six packages; verify [release status](https://github.com/AceDataCloud/LangChain/blob/main/RELEASE_STATUS.md) for actual uploaded versions. Existing `0.1.0rc1` packages are historical prereleases. Package publication and official LangChain directory approval are separate gates. No new graphical chat button or upstream default-provider registration is claimed.

## Install only the integration you need

Use Python 3.10+ in a virtual environment. Each service package installs only its own tool classes plus the shared runtime, not the other four services.

| Integration | Package / official registry destination | Guide |
| --- | --- | --- |
| Ace chat model | [`langchain-acedatacloud`](https://pypi.org/project/langchain-acedatacloud/) | [Chat model](#chat-without-a-custom-base-url) |
| Suno by Ace Data Cloud | [`langchain-suno-acedatacloud`](https://pypi.org/project/langchain-suno-acedatacloud/) | [suno](https://github.com/AceDataCloud/LangChain/blob/main/packages/suno/README.md) |
| Seedance by Ace Data Cloud | [`langchain-seedance-acedatacloud`](https://pypi.org/project/langchain-seedance-acedatacloud/) | [seedance](https://github.com/AceDataCloud/LangChain/blob/main/packages/seedance/README.md) |
| HappyHorse by Ace Data Cloud | [`langchain-happyhorse-acedatacloud`](https://pypi.org/project/langchain-happyhorse-acedatacloud/) | [happyhorse](https://github.com/AceDataCloud/LangChain/blob/main/packages/happyhorse/README.md) |
| GPT Image by Ace Data Cloud | [`langchain-gpt-image-acedatacloud`](https://pypi.org/project/langchain-gpt-image-acedatacloud/) | [gpt-image](https://github.com/AceDataCloud/LangChain/blob/main/packages/gpt-image/README.md) |
| Nano Banana by Ace Data Cloud | [`langchain-nano-banana-acedatacloud`](https://pypi.org/project/langchain-nano-banana-acedatacloud/) | [nano-banana](https://github.com/AceDataCloud/LangChain/blob/main/packages/nano-banana/README.md) |

```bash
python3 -m venv .venv
source .venv/bin/activate
# Stable version (after registry readback):
python -m pip install langchain-acedatacloud==0.1.0
# Or one service:
python -m pip install langchain-happyhorse-acedatacloud==0.1.0
```

For source installation, run `git clone --branch main https://github.com/AceDataCloud/LangChain.git`, `cd LangChain`, then `pip install -e packages/core -e packages/suno`. Package artifacts are not proof of official listing.

## Get the application API Key

1. [Register or sign in → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_readme_api_key). If no **General application** exists, choose **Initialize General Application**.
2. Open the General application. Copy its **API Key**, or choose **Manage Keys → Create** to make a separately named LangChain key. Review expiration, usage limitations and **Allowed APIs**. Allow both the generation and same-ID task query paths used below. Confirm service access, balance and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_readme_pricing). No trial allowance is promised.
3. Copy the raw token only, without `Bearer `, quotation marks or redacted characters. A `platform-...` account-management token cannot replace this application key.

![Copy the redacted application API Key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

The historical create-key image says `Dify tutorial`; name the actual key `LangChain <service>`. These are real Ace console screenshots reused from [SunoDify](https://github.com/AceDataCloud/SunoDify/tree/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial), retrieved 2026-10-18; later console layouts may differ. They show credential setup, not a LangChain GUI. Real tokens are redacted.

```bash
export ACEDATACLOUD_API_TOKEN='your application key'
```

PowerShell: `$env:ACEDATACLOUD_API_TOKEN='your application key'`. Keep the token in the environment or secret manager, never in a prompt or workflow export.

## Chat without a custom base URL

```python
from langchain_acedatacloud import ChatAceDataCloud

model = ChatAceDataCloud(model="gpt-4o-mini")
reply = model.invoke("Reply in one short sentence.")  # One paid API request.
print(reply.content)
print(reply.usage_metadata)  # Token counts, not charged Credits.
```

The named class owns Ace credential and endpoint defaults. Standard chat, async, stream and tool binding reuse LangChain's OpenAI protocol implementation. It fixes Chat Completions mode, disables automatic retries by default, and identifies traces as `acedatacloud`. Model-specific capabilities still depend on the selected model. For stream token counts use `stream_usage=True` only where supported.

Use `model.bind_tools([...])`, execute a returned local tool, and supply `ToolMessage` to complete a tool loop. Each model invocation may be charged; a tool selection plus final answer normally means two calls. This does **not** mean `init_chat_model(model_provider="acedatacloud")` is built into the upstream release. A maintainer-approved provider-registry entry is a separate goal.

## Add a single service to an agent

```python
from langchain_acedatacloud import AceAPIClient
from langchain_suno_acedatacloud import SunoToolkit

# Query-only by default: enabling a toolkit must not silently enable paid generation.
tools = SunoToolkit(client=AceAPIClient()).get_tools()
print([tool.name for tool in tools])
# ['suno_retrieve_task']
```

An application deliberately enables generation with `include_generation=True` after showing current prices and obtaining its user's authorization. Pass those BaseTool instances to your LangChain agent or invoke them directly. The client credential is not part of the LLM tool schema.

## Asynchronous results and billing

One generation-tool invocation submits one request with `async=true`, returns a task ID, and does not loop or retry. Query tools call the service's task endpoint with the **same** ID. A successful submission or preview URL is not terminal completion. The normalized result exposes `terminal` and `status`; a pending result must be queried again later, never regenerated merely to poll. Media URLs are exposed as final only after `finished_at`; raw API data remains available for diagnosis. The tools do not download remote media.

Inspect [Usage History](https://platform.acedata.cloud/console/usages?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_readme_usage) for actual Credits and uncertain submissions. Token counts and package downloads are not revenue. No integration test is configured to issue paid calls in CI.

## Troubleshooting

| Result | What to check |
| --- | --- |
| 401 / missing key | Use the raw application API Key and `ACEDATACLOUD_API_TOKEN`. |
| 403 | Service access, balance, expiry, usage/API restrictions and response policy details. |
| 429 | Reduce concurrency; no automatic paid retry is performed. |
| Pending / empty media | Query the same task ID; do not resubmit generation. |
| Timeout / 5xx | Check original task and Usage History before deciding on another paid request. |
| Unsupported provider in `init_chat_model` | Import `ChatAceDataCloud` directly; upstream default-provider registration is not claimed. |

## Development and contribution

```bash
pip install -r requirements-dev.txt
pip install -e packages/core
pip install --no-deps -e packages/suno -e packages/seedance -e packages/happyhorse -e packages/gpt-image -e packages/nano-banana
python scripts/check_packages.py
ruff check .
ruff format --check .
pytest
python scripts/build_packages.py
python -m twine check dist/*
```

The repository is a single source for shared transport/task behavior. Packages have independent identities, service names, schemas and listing materials. The [LangChain integration process](https://docs.langchain.com/oss/python/contributing/integrations-langchain) requires published packages and a listing issue; see `submissions/` for reviewable forms. No unsolicited manual listing PR or promotional message is sent.


## Official requests (2026-10-18)

These are submissions, not approved entries: [ChatAceDataCloud](https://github.com/langchain-ai/docs/issues/6809), [HappyHorse by Ace Data Cloud](https://github.com/langchain-ai/docs/issues/6810), [GPT Image by Ace Data Cloud](https://github.com/langchain-ai/docs/issues/6811), [Nano Banana by Ace Data Cloud](https://github.com/langchain-ai/docs/issues/6812). The [native default-provider request](https://github.com/langchain-ai/langchain/issues/41291) was automatically closed because programmatic submission is disallowed; it needs the official web template. No API resubmission or issue-type workaround is used. Suno and Seedance listing forms are submitted only after their public package installation is verified.
