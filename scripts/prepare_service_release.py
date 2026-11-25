"""Select one tested service distribution and verify its version and source bytes."""

import argparse
import hashlib
import json
import re
import shutil
import tarfile
import zipfile
from email.parser import BytesParser
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ("acemusic", "happyhorse", "gpt-image", "nano-banana", "suno", "seedance")


def prepare(service: str, version: str, artifacts: Path, output: Path) -> None:
    if service not in SERVICES or not re.fullmatch(r"\d+\.\d+\.\d+(?:rc\d+)?", version):
        raise ValueError("Choose one service and an exact release version")
    package = ROOT / "packages" / service
    project = tomllib.loads((package / "pyproject.toml").read_text())["project"]
    if project["version"] != version:
        raise ValueError("Requested version does not match the checked-out source")
    name = project["name"]
    stem = name.replace("-", "_") + "-" + version
    wheel = artifacts / (stem + "-py3-none-any.whl")
    sdist = artifacts / (stem + ".tar.gz")
    sources = {
        p.relative_to(package / "src").as_posix(): p.read_bytes()
        for p in (package / "src").rglob("*.py")
    }
    with zipfile.ZipFile(wheel) as archive:
        if {n for n in archive.namelist() if n.endswith(".py")} != set(sources):
            raise ValueError("Wheel Python files do not match the selected package")
        for path, content in sources.items():
            if archive.read(path) != content:
                raise ValueError(f"Wheel source mismatch: {path}")
        metadata = BytesParser().parsebytes(archive.read(stem + ".dist-info/METADATA"))
        if metadata["Name"] != name or metadata["Version"] != version:
            raise ValueError("Wheel metadata does not match the selected package")
    with tarfile.open(sdist) as archive:
        expected = {"src/" + path: content for path, content in sources.items()}
        expected.update(
            {
                path: (package / path).read_bytes()
                for path in ["pyproject.toml", "README.md", "LICENSE"]
            }
        )
        for path, content in expected.items():
            entry = archive.getmember(stem + "/" + path)
            if not entry.isfile():
                raise ValueError(f"Source distribution member is not a regular file: {path}")
            handle = archive.extractfile(entry)
            if handle is None or handle.read() != content:
                raise ValueError(f"Source distribution mismatch: {path}")
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError("Output directory must be empty")
    manifest = {"package": name, "version": version, "files": []}
    for path in [wheel, sdist]:
        shutil.copyfile(path, output / path.name)
        manifest["files"].append(
            {"name": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        )
    # Keep provenance outside the directory passed to twine.
    output.with_suffix(".json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Verified two {name} {version} distributions against source")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--service", required=True, choices=SERVICES)
    parser.add_argument("--version", required=True)
    parser.add_argument("--artifacts", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    prepare(args.service, args.version, args.artifacts, args.output)


if __name__ == "__main__":
    main()
