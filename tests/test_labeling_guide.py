"""Tests for corpus/LABELING.md."""

import json
from pathlib import Path

CORPUS = Path(__file__).resolve().parent.parent / "corpus"
GUIDE = CORPUS / "LABELING.md"


def _text() -> str:
    return GUIDE.read_text(encoding="utf-8")


def test_guide_exists() -> None:
    assert GUIDE.is_file()


def test_guide_mentions_every_feature() -> None:
    schema = json.loads((CORPUS / "schema.json").read_text(encoding="utf-8"))
    features = schema["properties"]["features"]["items"]["enum"]
    text = _text()
    for feature in features:
        assert f"`{feature}`" in text, feature


def test_guide_mentions_every_intent() -> None:
    intents = set()
    for f in (CORPUS / "data").glob("*.jsonl"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                intents.add(json.loads(line)["intent"])
    text = _text()
    assert intents
    for intent in intents:
        assert f"`{intent}`" in text, intent


def test_guide_linked_from_schema_and_readme() -> None:
    assert "LABELING.md" in (CORPUS / "SCHEMA.md").read_text(encoding="utf-8")
    readme = CORPUS / "README.md"
    if readme.exists():
        assert "LABELING.md" in readme.read_text(encoding="utf-8")
