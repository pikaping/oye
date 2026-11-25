import json
from pathlib import Path

import pytest

from corpus.loader import CorpusError, load_corpus, validate_entry

GOOD = {
    "id": "oye-0001",
    "text": "oye, quiero cancelar mi pedido",
    "intent": "cancel_order",
    "region": "es-ES",
    "features": ["filler"],
}


def write(tmp_path: Path, *lines: str) -> Path:
    p = tmp_path / "c.jsonl"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def test_loads_and_skips_blank_lines(tmp_path: Path) -> None:
    p = write(tmp_path, json.dumps(GOOD), "", "   ", json.dumps({**GOOD, "id": "oye-0002", "synthetic": True}))
    entries = load_corpus(p)
    assert [e.id for e in entries] == ["oye-0001", "oye-0002"]
    assert entries[0].synthetic is False
    assert entries[1].synthetic is True
    assert entries[0].features == ("filler",)


def test_invalid_json_reports_line(tmp_path: Path) -> None:
    p = write(tmp_path, json.dumps(GOOD), "", "{oops")
    with pytest.raises(CorpusError, match=r":3: invalid JSON"):
        load_corpus(p)


@pytest.mark.parametrize(
    "bad, msg",
    [
        ({k: v for k, v in GOOD.items() if k != "text"}, "missing required field 'text'"),
        ({**GOOD, "features": ["nope"]}, "unknown feature 'nope'"),
        ({**GOOD, "text": 5}, "'text' must be a string"),
        ({**GOOD, "features": "slang"}, "'features' must be a list"),
        ({**GOOD, "synthetic": "yes"}, "'synthetic' must be a boolean"),
        ({**GOOD, "id": "x1"}, "'id' must match"),
        ({**GOOD, "extra": 1}, "unknown field 'extra'"),
        ({**GOOD, "features": ["slang", "slang"]}, "duplicates"),
    ],
)
def test_invalid_entries_report_line(tmp_path: Path, bad: dict, msg: str) -> None:
    p = write(tmp_path, json.dumps(GOOD), json.dumps(bad))
    with pytest.raises(CorpusError, match=msg) as info:
        load_corpus(p)
    assert ":2:" in str(info.value)


@pytest.mark.parametrize(
    "bad, msg",
    [
        ({**GOOD, "text": ""}, "'text' must not be empty"),
        ({**GOOD, "region": ""}, "'region' must not be empty"),
        ({**GOOD, "features": [1]}, "only strings"),
    ],
)
def test_empty_and_non_string_values(bad: dict, msg: str) -> None:
    with pytest.raises(CorpusError, match=msg):
        validate_entry(bad)


def test_colloquial_text_with_typos_and_accents_roundtrips(tmp_path: Path) -> None:
    texts = [
        "q tal, xfa cancelame el pedio k no llego ni de coña",
        "oyeee tio, k pasa kon mi reembolso?? llevo semanas esperandooo",
        "ola buenas, kiero cambiar la direccion d envio, ta mal",
    ]
    lines = [
        json.dumps(
            {**GOOD, "id": f"oye-{i:04d}", "text": t, "features": ["typo", "abbreviation"]},
            ensure_ascii=False,
        )
        for i, t in enumerate(texts, start=1)
    ]
    entries = load_corpus(write(tmp_path, *lines))
    assert [e.text for e in entries] == texts
    assert entries[0].features == ("typo", "abbreviation")


def test_missing_file_raises_oserror(tmp_path: Path) -> None:
    with pytest.raises(OSError):
        load_corpus(tmp_path / "nope.jsonl")


def test_validate_entry_rejects_non_object() -> None:
    with pytest.raises(CorpusError):
        validate_entry([])
