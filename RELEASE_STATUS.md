# Release status — 2026-10-18

This is an explicitly published **0.1.0rc1 prerelease from the open implementation PR**, not a merged stable release. No upstream default-provider registration or LangChain official listing is claimed.

| Package | PyPI 0.1.0rc1 | Official LangChain listing |
| --- | --- | --- |
| langchain-acedatacloud | Published wheel; JSON/hash readback verified | [OPEN request](https://github.com/langchain-ai/docs/issues/6809), not approved |
| langchain-happyhorse-acedatacloud | Published wheel; JSON/hash readback verified | [OPEN request](https://github.com/langchain-ai/docs/issues/6810), not approved |
| langchain-gpt-image-acedatacloud | Published wheel; JSON/hash readback verified | [OPEN request](https://github.com/langchain-ai/docs/issues/6811), not approved |
| langchain-nano-banana-acedatacloud | Published wheel; JSON/hash readback verified | [OPEN request](https://github.com/langchain-ai/docs/issues/6812), not approved |
| langchain-suno-acedatacloud | Not published: upload returned HTTP 429 | Not eligible until publication |
| langchain-seedance-acedatacloud | Not published: upload returned HTTP 429 | Not eligible until publication |

Use an explicit `==0.1.0rc1` pin for published candidates. Bare pip installation may exclude prereleases. All six local wheels passed clean installation; the separate registry CI job checks the four public packages. The maintainer's local network cannot connect to files.pythonhosted.org, so local JSON/hash verification is not claimed as a registry download.

The source readmes in the immutable candidate wheels were written before this partial publication; this status page records subsequent changes. Package upload stopped at 429 and is not retried in a loop. Do not claim Suno/Seedance were published or submit false published-package confirmations.


Default `init_chat_model` selection is separately requested at https://github.com/langchain-ai/langchain/issues/41291. It was reproduced as unsupported on LangChain 1.4.6 and is not patched at import time. The feature form requires maintainer assignment before a registry PR.

All six immutable candidate wheel/sdist assets: https://github.com/AceDataCloud/LangChain/releases/tag/v0.1.0rc1 . The latest [registry install CI](https://github.com/AceDataCloud/LangChain/actions/runs/39061165755) successfully installed the four PyPI packages in a clean GitHub runner; local wheel-CDN failure is an environment limitation, not evidence that the packages are unavailable.
