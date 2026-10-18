"""Install/import exact public packages without credentials or API requests."""

import argparse
import importlib
import importlib.metadata
import re
import subprocess
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="0.1.0rc1")
    parser.add_argument("--all-services", action="store_true")
    parser.add_argument("--install", choices=["pypi", "github"])
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:rc[0-9]+)?", args.version):
        raise SystemExit("Expected an exact release version")

    services = [
        ("happyhorse", "HappyHorse"),
        ("gpt_image", "GPTImage"),
        ("nano_banana", "NanoBanana"),
    ]
    if args.all_services:
        services += [("suno", "Suno"), ("seedance", "Seedance")]
    packages = ["langchain-acedatacloud"] + [
        "langchain-" + slug.replace("_", "-") + "-acedatacloud" for slug, _ in services
    ]
    if args.install:
        targets = (
            [name + "==" + args.version for name in packages]
            if args.install == "pypi"
            else [
                "https://github.com/AceDataCloud/LangChain/releases/download/v"
                + args.version
                + "/"
                + name.replace("-", "_")
                + "-"
                + args.version
                + "-py3-none-any.whl"
                for name in packages
            ]
        )
        subprocess.run([sys.executable, "-m", "pip", "install", *targets], check=True)
    for name in packages:
        assert importlib.metadata.version(name) == args.version
        print(name, "installed version verified")
    runtime = importlib.import_module("langchain_acedatacloud")
    assert runtime.ChatAceDataCloud.__name__ == "ChatAceDataCloud"
    for slug, class_prefix in services:
        module = importlib.import_module("langchain_" + slug + "_acedatacloud")
        toolkit_class = getattr(module, class_prefix + "Toolkit")
        toolkit = toolkit_class(client=runtime.AceAPIClient("offline-placeholder"))
        assert len(toolkit.get_tools()) == 1
        print(toolkit_class.__name__, toolkit.get_tools()[0].name)


if __name__ == "__main__":
    main()
