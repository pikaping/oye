"""Checks the contribute-phrase issue form against the corpus schema."""

import json
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

ROOT = Path(__file__).resolve().parent.parent
FORM = ROOT / "ci" / "ISSUE_TEMPLATE" / "contribute-phrase.yml"


def _form() -> dict:
    return yaml.safe_load(FORM.read_text(encoding="utf-8"))


def _field(form: dict, field_id: str) -> dict:
    return next(b for b in form["body"] if b.get("id") == field_id)


def test_labels_and_config() -> None:
    assert _form()["labels"] == ["corpus", "phrase"]
    config = yaml.safe_load((FORM.parent / "config.yml").read_text(encoding="utf-8"))
    assert config["blank_issues_enabled"] is True


def test_required_fields() -> None:
    form = _form()
    assert form["name"] and form["description"]
    ids = {b.get("id") for b in form["body"]}
    assert {"text", "intent", "region", "features", "origin", "anonymized"} <= ids
    assert _field(form, "text")["validations"]["required"] is True
    assert "do not fix typos" in _field(form, "text")["attributes"]["description"]
    options = _field(form, "anonymized")["attributes"]["options"]
    assert all(o.get("required") for o in options)


def test_feature_checkboxes_match_schema() -> None:
    schema = json.loads((ROOT / "corpus" / "schema.json").read_text(encoding="utf-8"))
    enum = schema["properties"]["features"]["items"]["enum"]
    labels = [o["label"] for o in _field(_form(), "features")["attributes"]["options"]]
    assert sorted(labels) == sorted(enum)
    assert len(labels) == 10
