# LangChain integrations

This repository owns the Ace LangChain chat model and five independently installable service toolkits. Use an isolated checkout. Preserve the single HTTP/task implementation in the core package; service packages own only their typed contracts and branding. Never commit credentials or run paid tests without current explicit authorization.

Run `python scripts/check_packages.py`, `ruff check .`, `ruff format --check .`, and `pytest` for offline validation. CI uses test discovery. Build all six wheels with `python scripts/build_packages.py`. No automatic merge or package upload is configured.
