# Contributing to Oye

Thanks for helping us test agents with how people actually talk.

## Setting up your environment

Oye requires Python 3.12.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

All tests must pass before you start and before you open a pull request.

## Commits

- Keep commits small and focused on one change.
- Use [Conventional Commits](https://www.conventionalcommits.org/) in English:
  - `feat(test): add a runner option for custom corpus paths`
  - `fix(corpus): correct a malformed record in the greetings file`
  - `docs: clarify the installation steps`
- Every commit must leave the test suite green (`pytest`).

## Code and documentation

- Python 3.12 with type hints; tests use `pytest`.
- The Genkit plugin is written in TypeScript under `plugins/genkit/`.
- Code, docstrings and documentation are written in English.

## Corpus rules

The corpus lives in `corpus/data/*.jsonl`.

- Phrases are written in Spanish (colloquial, as people really speak).
- Phrases must be anonymized: no real names, phone numbers, emails, addresses or any other personal data.
- Never commit keys, tokens or credentials.
- Records must pass the corpus validator and schema.
- To suggest a phrase, use the [contribute-phrase issue form](ci/ISSUE_TEMPLATE/contribute-phrase.yml) (it will live in `.github/ISSUE_TEMPLATE/` once moved). Paste the text exactly as written, typos included.

## Proposing changes

1. Open an issue describing the bug or idea, so we can discuss it first.
2. Fork the repository and create a branch from `main`.
3. Make your changes with small, conventional commits and add or update tests.
4. Run `pytest` and make sure everything passes.
5. Open a pull request that references the issue and explains what and why.

## License

Oye is released under the Apache License 2.0. By contributing, you agree that your contributions are licensed under the same terms.
