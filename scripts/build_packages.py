"""Build every package into an explicit output directory. Never uploads artifacts."""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--outdir", type=Path, default=ROOT / "dist")
args = parser.parse_args()
for package in sorted((ROOT / "packages").iterdir()):
    subprocess.run(
        [sys.executable, "-m", "build", str(package), "--outdir", str(args.outdir.resolve())],
        check=True,
    )
