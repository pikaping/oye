"""Checks that the top-level repository docs keep their key content."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAGLINE = "Test your agents with how people actually talk."


def _read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_readme_has_exact_tagline() -> None:
    assert TAGLINE in _read("README.md")


def test_readme_mentions_license() -> None:
    assert "Apache License 2.0" in _read("README.md")


def test_readme_links_contributing_and_license() -> None:
    readme = _read("README.md")
    assert "](CONTRIBUTING.md)" in readme
    assert "](LICENSE)" in readme


def test_contributing_exists() -> None:
    assert (ROOT / "CONTRIBUTING.md").is_file()


def test_contributing_mentions_conventions() -> None:
    text = _read("CONTRIBUTING.md")
    assert "Conventional Commits" in text
    assert "pytest" in text
