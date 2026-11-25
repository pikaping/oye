import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "corpus" / "README.md"


def test_readme_exists_and_mentions_fields() -> None:
    text = README.read_text(encoding="utf-8")
    for field in ("id", "text", "intent", "region", "features", "synthetic"):
        assert f"`{field}`" in text


def test_root_readme_links_corpus_readme() -> None:
    assert "corpus/README.md" in (ROOT / "README.md").read_text(encoding="utf-8")


def test_loading_example_runs(monkeypatch) -> None:
    text = README.read_text(encoding="utf-8")
    block = re.search(r"```python\n(.*?)```", text, re.DOTALL)
    assert block
    monkeypatch.chdir(ROOT)
    exec(block.group(1), {})
