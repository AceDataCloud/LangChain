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
