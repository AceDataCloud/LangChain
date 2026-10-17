# Release status — 2026-10-18

This is an explicitly published **0.1.0rc1 prerelease from the open implementation PR**, not a merged stable release. No upstream default-provider registration or LangChain official listing is claimed.

| Package | PyPI 0.1.0rc1 | Official LangChain listing |
| --- | --- | --- |
| langchain-acedatacloud | Published wheel; JSON/hash readback verified | Submission being prepared |
| langchain-happyhorse-acedatacloud | Published wheel; JSON/hash readback verified | Submission being prepared |
| langchain-gpt-image-acedatacloud | Published wheel; JSON/hash readback verified | Submission being prepared |
| langchain-nano-banana-acedatacloud | Published wheel; JSON/hash readback verified | Submission being prepared |
| langchain-suno-acedatacloud | Not published: upload returned HTTP 429 | Not eligible until publication |
| langchain-seedance-acedatacloud | Not published: upload returned HTTP 429 | Not eligible until publication |

Use an explicit `==0.1.0rc1` pin for published candidates. Bare pip installation may exclude prereleases. All six local wheels passed clean installation; the separate registry CI job checks the four public packages. The maintainer's local network cannot connect to files.pythonhosted.org, so local JSON/hash verification is not claimed as a registry download.

The source readmes in the immutable candidate wheels were written before this partial publication; this status page records subsequent changes. Package upload stopped at 429 and is not retried in a loop. Do not claim Suno/Seedance were published or submit false published-package confirmations.
