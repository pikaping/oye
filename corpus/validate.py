"""Validation for Oye Corpus files. Never modifies entry text.

Library: ``find_duplicates`` and ``validate_paths`` (reports all problems).

Command line::

    python -m corpus.validate [--strict] [PATH ...]

Without paths it validates ``corpus/data/``. Paths may be files or
directories. Each problem is printed as ``file:line: code: message``, followed
by a summary. Exit code is 0 when there are no errors, 1 otherwise. Warnings
(near-duplicates) only fail with ``--strict``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from corpus.loader import CorpusError, Entry, validate_entry

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


@dataclass(frozen=True)
class Issue:
    """One problem found in a corpus file. ``severity`` is "error" or "warning"."""

    file: str
    line: int
    code: str
    message: str
    severity: str = "error"

    def __str__(self) -> str:
        return f"{self.file}:{self.line}: {self.severity} [{self.code}] {self.message}"


def validate_paths(paths: Iterable[str | Path]) -> list[Issue]:
    """Validate JSONL files without stopping at the first error.

    Reports invalid JSON, schema violations, non-UTF-8 files, surrounding
    whitespace or line breaks in text, and duplicates across all files.
    Near-duplicates are reported with severity "warning". Never modifies data.
    """
    issues: list[Issue] = []
    located: list[tuple[str, int, Entry]] = []
    expanded: list[str | Path] = []
    for path in paths:
        if Path(path).is_dir():
            found = sorted(Path(path).glob("*.jsonl"))
            if not found:
                issues.append(Issue(str(path), 0, "unreadable", "directory has no .jsonl files"))
            expanded.extend(found)
        else:
            expanded.append(path)
    for path in expanded:
        name = str(path)
        try:
            raw = Path(path).read_bytes()
        except OSError as exc:
            issues.append(Issue(name, 0, "unreadable", f"cannot read file: {exc.strerror or exc}"))
            continue
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            line = raw.count(b"\n", 0, exc.start) + 1
            issues.append(Issue(name, line, "not-utf8", f"file is not valid UTF-8: {exc.reason}"))
            continue
        for lineno, line_text in enumerate(content.split("\n"), start=1):
            if not line_text.strip():
                continue
            try:
                entry = validate_entry(json.loads(line_text))
            except json.JSONDecodeError as exc:
                issues.append(Issue(name, lineno, "invalid-json", f"invalid JSON: {exc.msg}"))
                continue
            except CorpusError as exc:
                issues.append(Issue(name, lineno, "invalid-entry", str(exc)))
                continue
            located.append((name, lineno, entry))
            if entry.text != entry.text.strip():
                issues.append(
                    Issue(name, lineno, "text-whitespace", "text has leading or trailing whitespace")
                )
            if "\n" in entry.text or "\r" in entry.text:
                issues.append(Issue(name, lineno, "text-newline", "text contains a line break"))

    groups: dict[tuple[str, str], list[tuple[str, int, Entry]]] = defaultdict(list)
    for item in located:
        groups[("id", item[2].id)].append(item)
        groups[("text", item[2].text)].append(item)
        groups[("norm", normalize_text(item[2].text))].append(item)
    for (group_kind, _key), group in groups.items():
        if len(group) < 2:
            continue
        problems, near = find_duplicates(e for _, _, e in group)
        # Each group only yields its own kind, so one occurrence is reported once.
        if group_kind == "id":
            msgs = [(m, "duplicate-id", "error") for m in problems if m.startswith("duplicate id")]
        elif group_kind == "text":
            msgs = [(m, "duplicate-text", "error") for m in problems if m.startswith("duplicate text")]
        else:
            msgs = [(m, "near-duplicate", "warning") for m in near]
        for msg, kind, severity in msgs:
            for file, lineno, _ in group[1:]:
                issues.append(Issue(file, lineno, kind, msg, severity))
    issues.sort(key=lambda i: (i.file, i.line, i.code))
    return issues


DEFAULT_DATA_DIR = Path(__file__).resolve().parent / "data"


def main(argv: list[str] | None = None) -> int:
    """Run the validator from the command line. Returns the process exit code."""
    parser = argparse.ArgumentParser(
        prog="python -m corpus.validate",
        description="Validate Oye Corpus JSONL files and report every problem found.",
    )
    parser.add_argument(
        "paths", nargs="*", help="JSONL files or directories (default: corpus/data/)"
    )
    parser.add_argument(
        "--strict", action="store_true", help="treat warnings (near-duplicates) as errors"
    )
    args = parser.parse_args(argv)
    paths: list[str | Path] = list(args.paths) or [DEFAULT_DATA_DIR]
    issues = validate_paths(paths)
    for issue in issues:
        print(f"{issue.file}:{issue.line}: {issue.code}: {issue.message}")
    errors = sum(1 for i in issues if i.severity == "error")
    warnings = len(issues) - errors
    print(f"{errors} error(s), {warnings} warning(s)")
    failed = errors > 0 or (args.strict and warnings > 0)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
