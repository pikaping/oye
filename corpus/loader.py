"""Minimal, dependency-free loader and validator for Oye Corpus JSONL files."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_SCHEMA_PATH = Path(__file__).with_name("schema.json")
_SCHEMA: dict[str, Any] = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))

REQUIRED_FIELDS: tuple[str, ...] = tuple(_SCHEMA["required"])
ALLOWED_FIELDS: frozenset[str] = frozenset(_SCHEMA["properties"])
FEATURES: frozenset[str] = frozenset(_SCHEMA["properties"]["features"]["items"]["enum"])
_ID_RE = re.compile(_SCHEMA["properties"]["id"]["pattern"])


class CorpusError(ValueError):
    """Raised when a corpus entry or file is invalid."""


@dataclass(frozen=True)
class Entry:
    """One corpus entry."""

    id: str
    text: str
    intent: str
    region: str
    features: tuple[str, ...]
    synthetic: bool = False


def validate_entry(obj: Any) -> Entry:
    """Validate a decoded JSON object and return it as an `Entry`.

    Raises `CorpusError` with a descriptive message on any violation.
    """
    if not isinstance(obj, dict):
        raise CorpusError(f"entry must be a JSON object, got {type(obj).__name__}")
    for name in REQUIRED_FIELDS:
        if name not in obj:
            raise CorpusError(f"missing required field '{name}'")
    for name in obj:
        if name not in ALLOWED_FIELDS:
            raise CorpusError(f"unknown field '{name}'")
    for name in ("id", "text", "intent", "region"):
        value = obj[name]
        if not isinstance(value, str):
            raise CorpusError(f"field '{name}' must be a string")
        if not value:
            raise CorpusError(f"field '{name}' must not be empty")
    if not _ID_RE.match(obj["id"]):
        raise CorpusError(f"field 'id' must match {_ID_RE.pattern}, got {obj['id']!r}")
    features = obj["features"]
    if not isinstance(features, list):
        raise CorpusError("field 'features' must be a list")
    for feature in features:
        if not isinstance(feature, str):
            raise CorpusError("field 'features' must contain only strings")
        if feature not in FEATURES:
            raise CorpusError(f"unknown feature {feature!r}")
    if len(set(features)) != len(features):
        raise CorpusError("field 'features' must not contain duplicates")
    synthetic = obj.get("synthetic", False)
    if not isinstance(synthetic, bool):
        raise CorpusError("field 'synthetic' must be a boolean")
    return Entry(
        id=obj["id"],
        text=obj["text"],
        intent=obj["intent"],
        region=obj["region"],
        features=tuple(features),
        synthetic=synthetic,
    )


def load_corpus(path: str | Path) -> list[Entry]:
    """Load a JSONL corpus file, skipping blank lines.

    Raises `CorpusError` prefixed with `<path>:<line>` on the first invalid line.
    """
    entries: list[Entry] = []
    with Path(path).open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            if not line.strip():
                continue
            try:
                entries.append(validate_entry(json.loads(line)))
            except json.JSONDecodeError as exc:
                raise CorpusError(f"{path}:{lineno}: invalid JSON: {exc.msg}") from exc
            except CorpusError as exc:
                raise CorpusError(f"{path}:{lineno}: {exc}") from exc
    return entries
