"""The README "Validating" section must exist and match the real command."""

import re
from pathlib import Path

from corpus import validate

ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "corpus" / "README.md"
README = README_PATH.read_text(encoding="utf-8")


def test_readme_exists_and_mentions_fields() -> None:
    text = README
    for field in ("id", "text", "intent", "region", "features", "synthetic"):
        assert f"`{field}`" in text


def test_root_readme_links_corpus_readme() -> None:
    assert "corpus/README.md" in (ROOT / "README.md").read_text(encoding="utf-8")


def test_loading_example_runs(monkeypatch) -> None:
    text = README
    block = re.search(r"```python\n(.*?)```", text, re.DOTALL)
    assert block
    monkeypatch.chdir(ROOT)
    exec(block.group(1), {})

def _section() -> str:
    assert "\n## Validating\n" in README
    return README.split("\n## Validating\n", 1)[1].split("\n## ", 1)[0]


def test_validating_section_documents_command_and_exit_codes() -> None:
    section = _section()
    assert "python -m corpus.validate" in section
    assert "--strict" in section
    assert "`0`" in section and "`1`" in section
    assert "near-duplicate" in section.lower()


def test_documented_command_matches_real_cli(capsys) -> None:
    import pytest

    with pytest.raises(SystemExit):
        validate.main(["--help"])
    help_out = capsys.readouterr().out
    assert "python -m corpus.validate" in help_out
    assert "--strict" in help_out


def test_schema_links_to_validating_section() -> None:
    schema = (ROOT / "corpus" / "SCHEMA.md").read_text(encoding="utf-8")
    assert "README.md#validating" in schema
