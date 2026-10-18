"""Import only public PyPI candidates. Never constructs a model or sends API calls."""

import importlib.metadata

from langchain_acedatacloud import AceAPIClient, ChatAceDataCloud
from langchain_gpt_image_acedatacloud import GPTImageToolkit
from langchain_happyhorse_acedatacloud import HappyHorseToolkit
from langchain_nano_banana_acedatacloud import NanoBananaToolkit

for name in [
    "langchain-acedatacloud",
    "langchain-happyhorse-acedatacloud",
    "langchain-gpt-image-acedatacloud",
    "langchain-nano-banana-acedatacloud",
]:
    assert importlib.metadata.version(name) == "0.1.0rc1"
    print(name, "installed from PyPI")
for cls in [HappyHorseToolkit, GPTImageToolkit, NanoBananaToolkit]:
    toolkit = cls(client=AceAPIClient("offline-placeholder"))
    assert len(toolkit.get_tools()) == 1
    print(cls.__name__, toolkit.get_tools()[0].name)
assert ChatAceDataCloud.__name__ == "ChatAceDataCloud"
