"""The exact command the CI workflow runs must pass on the shipped corpus."""

import subprocess
import sys
from pathlib import Path

from corpus.validate import main

ROOT = Path(__file__).resolve().parent.parent


def test_strict_validation_of_corpus_data_exits_zero() -> None:
    assert main(["--strict", str(ROOT / "corpus" / "data")]) == 0


def test_strict_validation_subprocess_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "corpus.validate", "--strict", "corpus/data"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
