"""Duplicate detection for Oye Corpus entries. Never modifies entry text."""

from __future__ import annotations

import re
import unicodedata
from collections import defaultdict
from collections.abc import Iterable

from corpus.loader import Entry

_PUNCT_RE = re.compile(r"[^\w\s]|_", re.UNICODE)
_SPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Return a comparison key: lowercase, no accents, no punctuation, collapsed spaces.

    Only used for comparison; the original text is never changed.
    """
    decomposed = unicodedata.normalize("NFD", text.lower())
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return _SPACE_RE.sub(" ", _PUNCT_RE.sub("", stripped)).strip()


def find_duplicates(entries: Iterable[Entry]) -> tuple[list[str], list[str]]:
    """Find duplicates among entries.

    Returns ``(problems, near_duplicates)``. ``problems`` reports repeated ids
    and exactly repeated texts. ``near_duplicates`` reports groups of entries
    whose texts differ but are equal once normalized.
    """
    items = list(entries)
    by_id: dict[str, list[Entry]] = defaultdict(list)
    by_text: dict[str, list[Entry]] = defaultdict(list)
    by_norm: dict[str, list[Entry]] = defaultdict(list)
    for e in items:
        by_id[e.id].append(e)
        by_text[e.text].append(e)
        by_norm[normalize_text(e.text)].append(e)

    problems: list[str] = []
    for id_, group in by_id.items():
        if len(group) > 1:
            problems.append(f"duplicate id {id_!r} ({len(group)} entries)")
    for text, group in by_text.items():
        if len(group) > 1:
            ids = ", ".join(e.id for e in group)
            problems.append(f"duplicate text {text!r} in ids: {ids}")

    near: list[str] = []
    for group in by_norm.values():
        if len({e.text for e in group}) > 1:
            desc = "; ".join(f"{e.id}: {e.text!r}" for e in group)
            near.append(f"near-duplicate texts: {desc}")
    return problems, near
