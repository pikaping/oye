"""Tests for the corpus validation CI workflow definition."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / "ci" / "corpus-validate.yml"


def _load() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def _triggers(data: dict) -> dict:
    # PyYAML (YAML 1.1) parses the bare key `on` as True.
    return data.get("on", data.get(True))


def _steps(data: dict) -> list[dict]:
    return [s for job in data["jobs"].values() for s in job["steps"]]


def test_workflow_exists_and_is_valid_yaml() -> None:
    assert WORKFLOW.is_file()
    assert isinstance(_load(), dict)


def test_triggers_on_pull_request() -> None:
    assert "pull_request" in _triggers(_load())


def test_paths_include_corpus() -> None:
    assert "corpus/**" in _triggers(_load())["pull_request"]["paths"]


def test_uses_python_312() -> None:
    versions = [
        str(s["with"]["python-version"])
        for s in _steps(_load())
        if "with" in s and "python-version" in s["with"]
    ]
    assert "3.12" in versions


def test_runs_strict_validation() -> None:
    runs = [s.get("run", "").strip() for s in _steps(_load())]
    assert "python -m corpus.validate --strict corpus/data" in runs


def test_runs_bare_pytest() -> None:
    runs = [s.get("run", "").strip() for s in _steps(_load())]
    assert "pytest" in runs


def test_does_not_reference_secrets() -> None:
    assert "secrets." not in WORKFLOW.read_text(encoding="utf-8")


def test_github_workflows_only_has_allowed_files() -> None:
    names = {p.name for p in (ROOT / ".github" / "workflows").iterdir()}
    assert names <= {"oye-daily.yml", "oye-linkedin.yml", "corpus-validate.yml"}
