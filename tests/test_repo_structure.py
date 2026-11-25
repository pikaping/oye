"""Sanity checks for the repository layout."""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_import_oye() -> None:
    import oye

    assert oye.__version__ == "0.0.1"


@pytest.mark.parametrize(
    "path",
    ["corpus/data", "oye/test", "oye/watch", "plugins/genkit", "starter", "docs", "tests"],
)
def test_directories_exist(path: str) -> None:
    assert (ROOT / path).is_dir()


@pytest.mark.parametrize("module", ["oye.test", "oye.watch"])
def test_subpackages_importable(module: str) -> None:
    import importlib

    assert importlib.import_module(module) is not None


def test_version_matches_pyproject() -> None:
    import tomllib

    import oye

    data = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert data["project"]["version"] == oye.__version__


def test_license_exists() -> None:
    assert (ROOT / "LICENSE").is_file()
