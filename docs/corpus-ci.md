# Corpus CI

A GitHub Actions workflow validates the corpus on every pull request that touches
`corpus/`, `tests/` or `pyproject.toml`, and on pushes to `main`.

## What it checks

1. `python -m corpus.validate --strict corpus/data`: every JSONL line is valid against the schema,
   there are no exact duplicates (errors) and no near-duplicates (warnings, treated as errors by `--strict`).
2. `pytest`: the full test suite.

## Running it locally

```
python -m corpus.validate --strict corpus/data
pytest
```

Both must exit with code 0, exactly as in CI.

## Reading failures

Each problem is printed as `file:line: code: message`, for example:

```
corpus/data/oye-es-001.jsonl:12: duplicate-text: ...
```

Open the file at that line number and fix the entry. All problems are reported in one run,
followed by a summary. The validator never modifies any text.

## Where the workflow lives

The workflow is staged in `ci/corpus-validate.yml`. Agents cannot write to `.github/`, so it stays there
until the author moves it to `.github/workflows/corpus-validate.yml`.
