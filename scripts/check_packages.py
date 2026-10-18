"""Check package identity and service-specific distribution metadata."""

import json
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog.json").read_text())
names = []
for path in sorted((ROOT / "packages").glob("*/pyproject.toml")):
    data = tomllib.loads(path.read_text())["project"]
    assert (path.parent / data["readme"]).is_file()
    assert (path.parent / "LICENSE").is_file()
    names.append(data["name"])
assert len(names) == len(set(names)) == 6
assert all(item["package"] in names for item in catalog["services"])
assert len({item["endpoint"] for item in catalog["services"]}) == 5
print("Six unique distributions; five distinct service contracts")
