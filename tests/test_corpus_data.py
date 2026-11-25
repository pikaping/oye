"""Tests for the shipped corpus data files."""

from pathlib import Path

from corpus.loader import load_corpus

DATA_DIR = Path(__file__).resolve().parent.parent / "corpus" / "data"
FILES = sorted(DATA_DIR.glob("*.jsonl"))


def _all_entries() -> list:
    return [e for f in FILES for e in load_corpus(f)]


def test_corpus_has_at_least_100_entries() -> None:
    assert len(_all_entries()) >= 100


def test_each_file_has_50_lines() -> None:
    for f in FILES:
        lines = [ln for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()]
        assert len(lines) == 50, f.name


def test_ids_unique_and_sequential_across_files() -> None:
    ids = [e.id for e in _all_entries()]
    assert len(set(ids)) == len(ids)
    assert ids == [f"oye-{i:04d}" for i in range(1, len(ids) + 1)]


def test_intent_and_region_diversity() -> None:
    entries = _all_entries()
    assert len({e.intent for e in entries}) >= 6
    assert len({e.region for e in entries}) >= 3


def test_no_duplicate_texts() -> None:
    texts = [" ".join(e.text.lower().split()) for e in _all_entries()]
    assert len(set(texts)) == len(texts)


def test_no_emails_phones_or_urls() -> None:
    import re

    email = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
    phone = re.compile(r"(?:\+?\d[\s.-]?){7,}")
    url = re.compile(r"https?://|www\.", re.I)
    for e in _all_entries():
        assert not email.search(e.text), e.id
        assert not phone.search(e.text), e.id
        assert not url.search(e.text), e.id


def test_informal_features_are_well_represented() -> None:
    entries = _all_entries()
    used = {f for e in entries for f in e.features}
    assert {"slang", "typo", "abbreviation", "ellipsis"} <= used
    informal = [e for e in entries if e.features]
    assert len(informal) >= len(entries) * 2 // 5


def test_all_entries_are_marked_synthetic() -> None:
    assert all(e.synthetic is True for e in _all_entries())
