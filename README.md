# Oye

Test your agents with how people actually talk.

Oye is an open source kit for testing conversational agents with real, colloquial Spanish.

## Components

- **Oye Corpus**: a dataset of colloquial Spanish (JSONL), with schema and validator. See [corpus/README.md](corpus/README.md).
- **Oye Test**: a command-line tester for agents, with a Genkit plugin.
- **Oye Watch**: analysis of conversations in production.
- **Oye Starter**: an agent template built with the Agent Development Kit (ADK).

## Project structure

```
corpus/          Oye Corpus (data/*.jsonl, schema, validator)
oye/             Python package (`oye` CLI)
  test/          Oye Test
  watch/         Oye Watch
plugins/genkit/  Oye plugin for Genkit (TypeScript)
starter/         Oye Starter (ADK template)
tests/           Test suite
docs/            Documentation
journal/         Daily session journal
posts/           Post plan and drafts
scripts/         Publishing scripts
```

## Status

Pre-alpha. Things change quickly and nothing is stable yet. See [ROADMAP.md](ROADMAP.md) for what is planned.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE).
