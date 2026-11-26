"""Tests for the corpus validator command line."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from corpus.validate import main


def _write(path: Path, lines: list[str]) -> Path:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_default_corpus_data_is_valid(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert "0 error(s)" in capsys.readouterr().out


def test_broken_file_reports_line_and_code(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    f = _write(tmp_path / "bad.jsonl", ["{not json"])
    assert main([str(f)]) == 1
    out = capsys.readouterr().out
    assert f"{f}:1: invalid-json:" in out
    assert "1 error(s)" in out


def test_directory_argument(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write(tmp_path / "a.jsonl", ["{oops"])
    assert main([str(tmp_path)]) == 1
    assert "a.jsonl:1: invalid-json" in capsys.readouterr().out


def test_empty_file_is_valid(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    f = _write(tmp_path / "ok.jsonl", [])
    assert main([str(f)]) == 0
    assert "0 error(s), 0 warning(s)" in capsys.readouterr().out


def _entry(id_: str, text: str) -> str:
    first = sorted(Path("corpus/data").glob("*.jsonl"))[0]
    data = json.loads(first.read_text(encoding="utf-8").splitlines()[0])
    data["id"] = id_
    data["text"] = text
    return json.dumps(data, ensure_ascii=False)


def test_near_duplicate_warning_and_strict(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    f = _write(tmp_path / "n.jsonl", [_entry("oye-9001", "Qué onda wey"), _entry("oye-9002", "que onda wey")])
    assert main([str(f)]) == 0
    out = capsys.readouterr().out
    assert "near-duplicate" in out and "1 warning(s)" in out
    assert main(["--strict", str(f)]) == 1


def test_nonexistent_path_is_an_error(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    missing = tmp_path / "no_existe.jsonl"
    assert main([str(missing)]) == 1
    out = capsys.readouterr().out
    assert f"{missing}:0: unreadable:" in out
    assert "1 error(s), 0 warning(s)" in out


def test_directory_without_jsonl_is_an_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1
    assert "unreadable" in capsys.readouterr().out


@pytest.mark.parametrize("strict", [False, True])
def test_only_errors_fail_with_or_without_strict(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], strict: bool
) -> None:
    f = _write(tmp_path / "e.jsonl", ["{mal", "otra cosa que no es json"])
    args = ["--strict", str(f)] if strict else [str(f)]
    assert main(args) == 1
    out = capsys.readouterr().out
    assert "2 error(s), 0 warning(s)" in out


def test_strict_on_clean_file_passes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    f = _write(tmp_path / "ok.jsonl", [_entry("oye-9101", "ke tal tio")])
    assert main(["--strict", str(f)]) == 0
    assert "0 error(s), 0 warning(s)" in capsys.readouterr().out


def test_summary_counts_errors_and_warnings_together(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    f = _write(
        tmp_path / "mix.jsonl",
        [
            _entry("oye-9201", "Qué onda wey"),
            _entry("oye-9202", "que onda wey"),
            "{roto",
        ],
    )
    assert main([str(f)]) == 1
    out = capsys.readouterr().out
    assert out.strip().splitlines()[-1] == "1 error(s), 1 warning(s)"
    assert f"{f}:3: invalid-json:" in out


def test_blank_lines_keep_real_line_numbers(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    f = _write(tmp_path / "b.jsonl", ["", "", "{x"])
    assert main([str(f)]) == 1
    assert f"{f}:3: invalid-json:" in capsys.readouterr().out


def test_multiple_files_are_all_reported(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    a = _write(tmp_path / "a.jsonl", ["{a"])
    b = _write(tmp_path / "b.jsonl", ["{b"])
    assert main([str(a), str(b)]) == 1
    out = capsys.readouterr().out
    assert f"{a}:1:" in out and f"{b}:1:" in out
    assert "2 error(s)" in out
