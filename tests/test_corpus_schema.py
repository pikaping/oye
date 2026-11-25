import json
from pathlib import Path

CORPUS = Path(__file__).resolve().parent.parent / "corpus"


def load_schema() -> dict:
    return json.loads((CORPUS / "schema.json").read_text(encoding="utf-8"))


def test_schema_required_fields() -> None:
    schema = load_schema()
    assert set(schema["required"]) == {"id", "text", "intent", "region", "features"}
    assert schema["properties"]["synthetic"]["default"] is False


def test_schema_features_closed_set() -> None:
    enum = load_schema()["properties"]["features"]["items"]["enum"]
    assert set(enum) == {
        "slang", "ellipsis", "typo", "diminutive",
        "code-switching", "filler", "abbreviation",
    }


def test_schema_synthetic_is_boolean_default_false_and_optional() -> None:
    schema = load_schema()
    synthetic = schema["properties"]["synthetic"]
    assert synthetic["type"] == "boolean"
    assert synthetic["default"] is False
    assert "synthetic" not in schema["required"]


def test_schema_features_is_unique_array_with_closed_enum() -> None:
    features = load_schema()["properties"]["features"]
    assert features["type"] == "array"
    assert features.get("uniqueItems") is True
    assert isinstance(features["items"]["enum"], list)
    assert len(features["items"]["enum"]) == len(set(features["items"]["enum"]))


def test_schema_is_closed_and_id_pattern() -> None:
    import re

    schema = load_schema()
    assert schema["additionalProperties"] is False
    assert set(schema["properties"]) == {
        "id", "text", "intent", "region", "features", "synthetic",
    }
    pattern = re.compile(schema["properties"]["id"]["pattern"])
    assert pattern.match("oye-0001")
    assert pattern.match("oye-12345")
    assert not pattern.match("oye-12")
    assert not pattern.match("oye-ab12")
    assert not pattern.match("xoye-0001")


def test_schema_md_documents_every_feature_and_field() -> None:
    doc = (CORPUS / "SCHEMA.md").read_text(encoding="utf-8")
    schema = load_schema()
    for feature in schema["properties"]["features"]["items"]["enum"]:
        assert f"`{feature}`" in doc
    for field in schema["properties"]:
        assert f"`{field}`" in doc


def test_schema_md_example_uses_valid_features_and_types() -> None:
    lines = (CORPUS / "SCHEMA.md").read_text(encoding="utf-8").splitlines()
    entry = json.loads([l for l in lines if l.startswith('{"id"')][0])
    schema = load_schema()
    assert set(entry) <= set(schema["properties"])
    assert isinstance(entry["features"], list)
    assert set(entry["features"]) <= set(schema["properties"]["features"]["items"]["enum"])
    assert isinstance(entry["synthetic"], bool)


def test_schema_md_has_valid_example() -> None:
    lines = (CORPUS / "SCHEMA.md").read_text(encoding="utf-8").splitlines()
    examples = [l for l in lines if l.startswith('{"id"')]
    assert examples
    entry = json.loads(examples[0])
    assert set(load_schema()["required"]) <= set(entry)
