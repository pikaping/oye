# Oye Corpus format

Each file in `corpus/data/` is JSONL: one JSON object per line, UTF-8.
The machine-readable definition is [`schema.json`](schema.json) (JSON Schema).
For how to label each field and feature, see the [labeling guide](LABELING.md).

| Field       | Type      | Required | Description |
|-------------|-----------|----------|-------------|
| `id`        | string    | yes      | Unique id, `oye-` plus at least 4 digits (e.g. `oye-0001`). |
| `text`      | string    | yes      | The utterance, in colloquial Spanish, anonymized. |
| `intent`    | string    | yes      | What the speaker wants (e.g. `cancel_order`). |
| `region`    | string    | yes      | `es-ES`, `es-MX`, `es-AR`, `neutral`, ... |
| `features`  | string[]  | yes      | Closed set: `slang`, `ellipsis`, `typo`, `diminutive`, `code-switching`, `filler`, `abbreviation`, `emoji`, `repeated-punctuation`, `missing-opening-mark`. See [Features](#features). |
| `synthetic` | boolean   | no       | `true` if generated rather than collected. Defaults to `false`. |

## Features

| Feature | Definition | Example |
|---------|------------|---------|
| `slang` | Informal or regional vocabulary. | `ostia q me ha llegado otra cosa` |
| `ellipsis` | Omitted words or trailing-off; includes telegraphic phrases (no verb or subject). | `el producto ha llegado roto y encima tarde...`, `cita jueves tarde` |
| `typo` | Omitted accents, swapped letters, missing capitals. | `Cuanto me queda en la cuenta?` |
| `diminutive` | Diminutive suffixes. | `un momentito` |
| `code-switching` | Mixing Spanish with another language. | `me hace falta el refund` |
| `filler` | Discourse fillers and openers. | `a ver es que...` |
| `abbreviation` | Shortened words or SMS-style spellings. | `q`, `porfa`, `x la tarde` |
| `emoji` | Contains one or more emoji. | `me ha llegado otra cosa 🤣` |
| `repeated-punctuation` | Repeated `?`, `!` or `.` marks (`??`, `!!`, `...`). | `ok perfe, gracias!!` |
| `missing-opening-mark` | A question (or exclamation) lacking the opening `¿` (or `¡`). | `A que hora abris mañana?` |

## Example

```json
{"id": "oye-0001", "text": "oye, quiero cancelar mi pedido, ¿se puede o k?", "intent": "cancel_order", "region": "es-ES", "features": ["filler", "slang", "typo"], "synthetic": false}
```

Phrases must not contain real names, phone numbers, emails or other personal data.
