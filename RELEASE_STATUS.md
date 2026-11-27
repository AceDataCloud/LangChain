# Current PyPI distributions

All eight packages install together in a fresh environment. The [public artifact and LangChain runtime check](https://github.com/AceDataCloud/LangChain/actions/runs/46073698948) checked both distribution hashes, the service artwork, and synchronous and asynchronous native tool entrypoints using controlled HTTP responses. The [ACE Music](https://github.com/langchain-ai/docs/issues/8168) and [Google Search](https://github.com/langchain-ai/docs/issues/8169) directory requests are tracked independently from package publication.

| Package | PyPI version |
| --- | --- |
| `langchain-acedatacloud` | [0.1.1](https://pypi.org/project/langchain-acedatacloud/0.1.1/) |
| `langchain-acemusic-acedatacloud` | [0.1.1](https://pypi.org/project/langchain-acemusic-acedatacloud/0.1.1/) |
| `langchain-suno-acedatacloud` | [0.1.1](https://pypi.org/project/langchain-suno-acedatacloud/0.1.1/) |
| `langchain-seedance-acedatacloud` | [0.1.1](https://pypi.org/project/langchain-seedance-acedatacloud/0.1.1/) |
| `langchain-happyhorse-acedatacloud` | [0.1.1](https://pypi.org/project/langchain-happyhorse-acedatacloud/0.1.1/) |
| `langchain-gpt-image-acedatacloud` | [0.1.2](https://pypi.org/project/langchain-gpt-image-acedatacloud/0.1.2/) |
| `langchain-nano-banana-acedatacloud` | [0.1.1](https://pypi.org/project/langchain-nano-banana-acedatacloud/0.1.1/) |
| `langchain-serp-acedatacloud` | [0.1.0](https://pypi.org/project/langchain-serp-acedatacloud/0.1.0/) |

# ACE Music 0.1.0

The [PyPI release](https://pypi.org/project/langchain-acemusic-acedatacloud/0.1.0/) offers a wheel and source distribution. A [clean Python 3.12 install](https://github.com/AceDataCloud/LangChain/actions/runs/46068069852) verified the native toolkit with LangChain Core, including synchronous and asynchronous retrieval using controlled responses. By default `get_tools()` exposes `acemusic_retrieve_task`. Generation requires `include_generation=True`. The [LangChain docs request](https://github.com/langchain-ai/docs/issues/8168) tracks the separate directory review.

# GPT Image 0.1.1 contract update

The GPT Image service package independently advances to 0.1.1 with 24 model IDs, eight quality values and DALL-E parameter validation. Core and the other four services retain 0.1.0. Existing five-model defaults are preserved; newly supported models omit optional quality/size unless supplied. The shared HTTP/task runtime is unchanged. Source validation is offline; publication and paid image acceptance are separate steps. The release verification workflow accepts `service=gpt-image` to install this exact independent version from PyPI and GitHub.

# Release status — 2026-10-20

Source PRs #1/#2/#3 are merged. Stable [v0.1.0](https://github.com/AceDataCloud/LangChain/releases/tag/v0.1.0) contains six wheel/source packages. **All six packages now also exist on PyPI at 0.1.0 with both wheel and source archive.** Historical 429 creation-quota failures are resolved for these packages; no repeated upload or replacement account was used.

| Distribution | PyPI 0.1.0 | Official LangChain discovery |
| --- | --- | --- |
| langchain-acedatacloud | wheel+sdist published | [chat PR#6839 merged](https://github.com/langchain-ai/docs/pull/6839), public chat directory verified |
| langchain-happyhorse-acedatacloud | wheel+sdist published | [PR#6840 merged](https://github.com/langchain-ai/docs/pull/6840), public tools directory verified |
| langchain-gpt-image-acedatacloud | wheel+sdist published | [PR#6836 merged](https://github.com/langchain-ai/docs/pull/6836), public tools directory verified |
| langchain-nano-banana-acedatacloud | wheel+sdist published | [PR#6828 merged](https://github.com/langchain-ai/docs/pull/6828), public tools directory verified |
| langchain-suno-acedatacloud | wheel+sdist published 2026-10-20 | [listing request#6877](https://github.com/langchain-ai/docs/issues/6877), pending |
| langchain-seedance-acedatacloud | wheel+sdist published 2026-10-20 | [listing request#6878](https://github.com/langchain-ai/docs/issues/6878), pending |

The newly published Suno/Seedance files exactly match the already-reviewed stable GitHub artifacts and source commit `04dcc0bc9e9b90d73a48ce2ee150c88de6c6d85d`. Upload was serial through the existing authorized publisher; all four upload responses were HTTP200, no429/Retry-After. Previously public packages were not re-uploaded.

[Verify published release#39321983859](https://github.com/AceDataCloud/LangChain/actions/runs/39321983859) passed with all_pypi=true: a fresh runner used ordinary pip to install all six exact 0.1.0 packages and loaded each query-only Toolkit. A separate fresh runner installed all six GitHub release wheels. Additional free input-schema checks verified Suno/Seedance's four native tools exclude credential fields and generation remains explicitly enabled by the application. No model/media request, automatic polling or paid generation was performed.

The official [chat](https://docs.langchain.com/oss/python/integrations/chat) and [tools](https://docs.langchain.com/oss/python/integrations/tools) live pages were read back 2026-10-20. Package downloads and directory badges are not user/revenue figures. Official listing is not default factory registration or featured placement.

Default `init_chat_model` support remains unimplemented upstream. Request [#41291](https://github.com/langchain-ai/langchain/issues/41291) was auto-closed for programmatic submission and requires the [official web feature template](https://github.com/langchain-ai/langchain/issues/new?template=feature-request.yml). Do not bypass it with API metadata or another identity. Historical v0.1.0rc1 stays immutable. Paid media-terminal/unique-bill and signup-to-first-call attribution acceptance remain separate.

## Independent service publishing

The manually dispatched `Publish one service package` workflow reuses this repository's existing organization `PYPI_TOKEN`. It never runs automatically on push. Supply the service, its exact declared version and a successful `CI` push run ID for the same main-branch commit. It selects only that service's two distributions from the tested Python 3.12 artifact, checks their package metadata and source bytes, uploads without skipping existing versions, and install-verifies the public package. Core and other services are not uploaded. The distribution hashes remain attached to the workflow run; create the matching GitHub release from those exact files and run `Verify published release` with the service selector.

PyPI can accept both files before its install index exposes the new version. The publisher retries only public installation/import verification for a bounded interval after upload; it never retries the upload step. If verification still fails, inspect the existing public files and run `Verify published release` separately after resolving the cause. Do not rerun an upload to an already published version.
