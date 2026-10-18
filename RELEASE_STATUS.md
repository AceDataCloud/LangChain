# Release status — 2026-10-19

Source PRs [#1](https://github.com/AceDataCloud/LangChain/pull/1) and [#2](https://github.com/AceDataCloud/LangChain/pull/2) are merged. Stable [v0.1.0](https://github.com/AceDataCloud/LangChain/releases/tag/v0.1.0) contains all six wheel/source packages. This does not mean upstream default Provider or official directory approval.

| Distribution | PyPI0.1.0 | GitHub0.1.0 |
| --- | --- | --- |
| langchain-acedatacloud | wheel+sdist, hashes verified | wheel+sdist |
| langchain-happyhorse-acedatacloud | wheel+sdist, hashes verified | wheel+sdist |
| langchain-gpt-image-acedatacloud | wheel+sdist, hashes verified | wheel+sdist |
| langchain-nano-banana-acedatacloud | wheel+sdist, hashes verified | wheel+sdist |
| langchain-suno-acedatacloud | not published: new-project429 quota | wheel+sdist |
| langchain-seedance-acedatacloud | not published: new-project429 quota | wheel+sdist |

Use ==0.1.0 for public PyPI packages. Suno/Seedance guides install the shared core and selected service wheel from GitHub. Existing PyPI identity can publish the four existing projects; the other two face quota, not a need for a new account. Do not loop retries or create an alternate identity.

The manual Verify published release workflow installs the public four from PyPI and all six GitHub wheels in separate fresh environments. all_pypi is enabled only when the missing projects are truly public. Neither check sends API requests.

Official requests remain OPEN/unapproved: chat https://github.com/langchain-ai/docs/issues/6809 , HappyHorse https://github.com/langchain-ai/docs/issues/6810 , GPT Image https://github.com/langchain-ai/docs/issues/6811 , Nano Banana https://github.com/langchain-ai/docs/issues/6812 . Default Provider request https://github.com/langchain-ai/langchain/issues/41291 was auto-closed for programmatic submission: use https://github.com/langchain-ai/langchain/issues/new?template=feature-request.yml through the coordinator's normal approved session, with no API/type bypass.

Historical v0.1.0rc1 is immutable. No new paid task, media-terminal/unique-bill or signup-to-first-call attribution acceptance is claimed by this release.
