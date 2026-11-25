# Oye Corpus format

Each file in `corpus/data/` is JSONL: one JSON object per line, UTF-8.
The machine-readable definition is [`schema.json`](schema.json) (JSON Schema).

| Field       | Type      | Required | Description |
|-------------|-----------|----------|-------------|
| `id`        | string    | yes      | Unique id, `oye-` plus at least 4 digits (e.g. `oye-0001`). |
| `text`      | string    | yes      | The utterance, in colloquial Spanish, anonymized. |
| `intent`    | string    | yes      | What the speaker wants (e.g. `cancel_order`). |
| `region`    | string    | yes      | `es-ES`, `es-MX`, `es-AR`, `neutral`, ... |
| `features`  | string[]  | yes      | Closed set: `slang`, `ellipsis`, `typo`, `diminutive`, `code-switching`, `filler`, `abbreviation`. |
| `synthetic` | boolean   | no       | `true` if generated rather than collected. Defaults to `false`. |

## Example

```json
{"id": "oye-0001", "text": "oye, quiero cancelar mi pedido, ¿se puede o k?", "intent": "cancel_order", "region": "es-ES", "features": ["filler", "slang", "typo"], "synthetic": false}
```

Phrases must not contain real names, phone numbers, emails or other personal data.
