"""Tests for corpus.validate.validate_paths."""

from __future__ import annotations

import json
from pathlib import Path

from corpus.validate import validate_paths


def _row(id_: str, text: str, **extra: object) -> str:
    obj = {"id": id_, "text": text, "intent": "saludo", "region": "es-ES", "features": []}
    obj.update(extra)
    return json.dumps(obj, ensure_ascii=False)


def test_real_corpus_has_no_errors() -> None:
    files = sorted(Path("corpus/data").glob("*.jsonl"))
    assert files
    errors = [i for i in validate_paths(files) if i.severity == "error"]
    assert errors == [], "\n".join(map(str, errors))


def test_multiple_errors_with_line_numbers(tmp_path: Path) -> None:
    a = tmp_path / "a.jsonl"
    b = tmp_path / "b.jsonl"
    a.write_text(
        "\n".join(
            [
                _row("oye-0001", "ola q tal"),
                "{not json",
                '{"id": "oye-0002"}',
                _row("oye-0003", " espacio sobrante "),
                _row("oye-0004", "salto\ndentro"),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    b.write_text(
        _row("oye-0001", "otra cosa") + "\n" + _row("oye-0005", "ola q tal") + "\n",
        encoding="utf-8",
    )
    got = {(Path(i.file).name, i.line, i.code) for i in validate_paths([a, b])}
    assert ("a.jsonl", 2, "invalid-json") in got
    assert ("a.jsonl", 3, "invalid-entry") in got
    assert ("a.jsonl", 4, "text-whitespace") in got
    assert ("a.jsonl", 5, "text-newline") in got
    assert ("b.jsonl", 1, "duplicate-id") in got
    assert ("b.jsonl", 2, "duplicate-text") in got


def test_near_duplicate_is_warning(tmp_path: Path) -> None:
    f = tmp_path / "n.jsonl"
    f.write_text(_row("oye-0001", "Qué tal") + "\n" + _row("oye-0002", "que tal!") + "\n")
    issues = validate_paths([f])
    assert [(i.line, i.code, i.severity) for i in issues] == [(2, "near-duplicate", "warning")]


def test_non_utf8_file(tmp_path: Path) -> None:
    f = tmp_path / "bad.jsonl"
    f.write_bytes(_row("oye-0001", "hola").encode() + b"\n\xff\xfe\n")
    issues = validate_paths([f])
    assert [(i.line, i.code) for i in issues] == [(2, "not-utf8")]


def test_empty_file_has_no_issues(tmp_path: Path) -> None:
    f = tmp_path / "empty.jsonl"
    f.write_text("")
    assert validate_paths([f]) == []


def test_no_paths_has_no_issues() -> None:
    assert validate_paths([]) == []


def test_blank_lines_are_skipped_but_counted(tmp_path: Path) -> None:
    f = tmp_path / "blank.jsonl"
    f.write_text("\n   \n" + _row("oye-0001", "ola q tal") + "\n\n{roto\n", encoding="utf-8")
    issues = validate_paths([f])
    assert [(i.line, i.code) for i in issues] == [(5, "invalid-json")]


def test_crlf_line_endings_are_accepted(tmp_path: Path) -> None:
    f = tmp_path / "crlf.jsonl"
    f.write_bytes((_row("oye-0001", "ola q tal") + "\r\n" + _row("oye-0002", "nose xq") + "\r\n").encode())
    assert validate_paths([f]) == []


def test_directory_is_reported_not_crash(tmp_path: Path) -> None:
    issues = validate_paths([tmp_path])
    assert len(issues) == 1
    assert issues[0].severity == "error"
    assert issues[0].file == str(tmp_path)


def test_missing_file_is_reported_not_crash(tmp_path: Path) -> None:
    issues = validate_paths([tmp_path / "nope.jsonl"])
    assert len(issues) == 1
    assert issues[0].severity == "error"


def test_duplicates_across_files_blame_later_file(tmp_path: Path) -> None:
    a = tmp_path / "a.jsonl"
    b = tmp_path / "b.jsonl"
    a.write_text(_row("oye-0001", "ola q tal") + "\n")
    b.write_text(_row("oye-0002", "ola q tal") + "\n")
    issues = validate_paths([a, b])
    assert [(Path(i.file).name, i.line, i.code) for i in issues] == [("b.jsonl", 1, "duplicate-text")]


def test_issue_str_format_and_str_paths(tmp_path: Path) -> None:
    f = tmp_path / "x.jsonl"
    f.write_text("{roto\n")
    (issue,) = validate_paths([str(f)])
    assert str(issue).startswith(f"{f}:1: error [invalid-json] ")


def test_valid_file_after_invalid_one_is_still_checked(tmp_path: Path) -> None:
    bad = tmp_path / "bad.jsonl"
    ok = tmp_path / "ok.jsonl"
    bad.write_bytes(b"\xff\n")
    ok.write_text("{roto\n")
    codes = {(Path(i.file).name, i.code) for i in validate_paths([bad, ok])}
    assert codes == {("bad.jsonl", "not-utf8"), ("ok.jsonl", "invalid-json")}
