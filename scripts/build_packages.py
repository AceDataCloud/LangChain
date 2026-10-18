"""Build every independently installable package; no upload or live API calls."""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for package in sorted((ROOT / "packages").iterdir()):
    subprocess.run(
        ["python", "-m", "build", str(package), "--outdir", str(ROOT / "dist")], check=True
    )
