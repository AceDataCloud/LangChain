# Ace provider factory: upstream review boundary

Goal: allow `init_chat_model("acedatacloud:gpt-4o-mini")` after installing the published integration package.

Current upstream `_BUILTIN_PROVIDERS` has no external entry-point hook. A future accepted registration would map `acedatacloud` to (`langchain_acedatacloud`, `ChatAceDataCloud`, `_call`) and append its package to the documented provider list. Tests would verify the provider-prefixed and explicit `model_provider` forms without changing inference for `gpt-*` names. Never redirect default OpenAI names to Ace or monkey-patch LangChain at import time.

Official policy on 2026-10-18: new implementations are independent packages, not monorepo integration PRs. The [maintainer response to a comparable provider request](https://github.com/langchain-ai/langchain/issues/36269#issuecomment-4194987536) directs new providers to their own repository and PyPI. The [contribution rules](https://docs.langchain.com/oss/python/contributing/overview) require prior maintainer approval for larger contributions. Therefore no unrequested provider-registry PR is submitted. Publish/review the independently tested package, apply for the allowed [integration listing](https://github.com/langchain-ai/docs/issues/new?template=06-integration-submission.yml), and only submit a registry patch if maintainers approve it.

The direct `ChatAceDataCloud` class is a real BaseChatModel-compatible provider with Ace endpoint/auth defaults. It is a distinct milestone from upstream built-in selection; do not label it as the latter.
