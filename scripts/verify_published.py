"""Import only public PyPI candidates. Never constructs a model or sends API calls."""

import argparse
import importlib.metadata

from langchain_acedatacloud import AceAPIClient, ChatAceDataCloud
from langchain_gpt_image_acedatacloud import GPTImageToolkit
from langchain_happyhorse_acedatacloud import HappyHorseToolkit
from langchain_nano_banana_acedatacloud import NanoBananaToolkit

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--version", default="0.1.0rc1")
parser.add_argument("--all-services", action="store_true")
args = parser.parse_args()

packages = [
    "langchain-acedatacloud",
    "langchain-happyhorse-acedatacloud",
    "langchain-gpt-image-acedatacloud",
    "langchain-nano-banana-acedatacloud",
]
if args.all_services:
    packages += ["langchain-suno-acedatacloud", "langchain-seedance-acedatacloud"]
for name in packages:
    assert importlib.metadata.version(name) == args.version
    print(name, "installed from PyPI")
for cls in [HappyHorseToolkit, GPTImageToolkit, NanoBananaToolkit]:
    toolkit = cls(client=AceAPIClient("offline-placeholder"))
    assert len(toolkit.get_tools()) == 1
    print(cls.__name__, toolkit.get_tools()[0].name)
assert ChatAceDataCloud.__name__ == "ChatAceDataCloud"

if args.all_services:
    from langchain_seedance_acedatacloud import SeedanceToolkit
    from langchain_suno_acedatacloud import SunoToolkit

    for cls in [SunoToolkit, SeedanceToolkit]:
        toolkit = cls(client=AceAPIClient("offline-placeholder"))
        assert len(toolkit.get_tools()) == 1
        print(cls.__name__, toolkit.get_tools()[0].name)
