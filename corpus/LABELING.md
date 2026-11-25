# Oye Corpus labeling guide

How to label entries in `corpus/data/*.jsonl`. The format is defined in [`SCHEMA.md`](SCHEMA.md)
and [`schema.json`](schema.json). Examples below are illustrative; none contains personal data.

## Golden rule: do not fix the text

Never correct the text: the typos are the value of the phrase. Keep missing accents, swapped letters,
lowercase sentence starts, missing `¿`/`¡`, odd spacing and SMS spelling exactly as written.
Label the mistakes (`typo`, `missing-opening-mark`, ...) instead of repairing them.

## Features

Pick every feature that applies, from this closed set. An entry may have an empty list only if it is plain, standard Spanish.

### `slang`
Informal or regional vocabulary.
- Positive: `cuanta plata me queda, che`, `ostia q me ha llegado otra cosa`.
- Borderline: `oye` or `anda` alone are fillers, not slang. Mild words like `vale` are not slang.

### `ellipsis`
Omitted words, telegraphic phrasing, or trailing off.
- Positive: `cita jueves tarde`, `saldo`, `se puede anular si ya pone enviado o ya no`.
- Positive: `el producto ha llegado roto y encima tarde...` (trailing `...` that leaves the idea open; also `repeated-punctuation`).
- Borderline: a `...` in the middle of a complete sentence that does not trail off is only `repeated-punctuation`; add `ellipsis` when the sentence trails off or drops words.

### `typo`
Omitted accents, swapped or changed letters, missing capitals where expected.
- Positive: `cancela el pedio ya`, `Cuanto me queda en la cuenta?`, `Cancelame` (missing accent).
- Borderline: all-lowercase text typed on purpose in a chat style counts as `typo` (missing capitals). Deliberate SMS spellings (`q`, `k`) are `abbreviation`, not `typo`.

### `diminutive`
Diminutive suffixes (-ito, -ita, -illo).
- Positive: `un momentito`, `una cosita rapida`.
- `ahorita` is a diminutive in Mexico: label it.
- Borderline: lexicalized words (`cafetería`) and names of things that only look diminutive (`bolsillo`) are not labeled.

### `code-switching`
Spanish mixed with another language.
- Positive: `me hace falta el refund`, `quiero hacer el checkout`.
- Borderline: widely adopted loanwords (`email`, `wifi`) are not labeled; brand names are not labeled.

### `filler`
Discourse fillers and openers that carry no request.
- Positive: `a ver es que...`, `eh, me podrias decir`, `oye,`.
- Borderline: a greeting that is the whole request (`hola`) is the `greeting` intent, not a filler.

### `abbreviation`
Shortened words or SMS-style spelling.
- Positive: `q`, `porfa`, `x la tarde`, `cta`, `pls`.
- Borderline: `xd` and similar chat interjections count as `abbreviation`.

### `emoji`
Contains one or more emoji.
- Positive: `me ha llegado otra cosa 🤣`.
- Borderline: text emoticons such as `:)` are not emoji; label them `slang` only if they are informal in context.

### `repeated-punctuation`
Repeated `?`, `!` or `.` (`??`, `!!`, `...`).
- Positive: `ok perfe, gracias!!`, `se puede??`, `llego roto...`.
- Borderline: a single `!` or `?` is not repeated. A normal full stop is not labeled.

### `missing-opening-mark`
A question or exclamation lacking the opening `¿` or `¡`.
- Positive: `A que hora abris mañana?`, `gracias por todo!`.
- Borderline: if the text has no question at all, do not label. If the opening mark is present, do not label, even if the closing one is missing.

## Intents

Intents used in `corpus/data` (snake_case):

- `book_appointment`
- `cancel_order`
- `check_balance`
- `complaint`
- `farewell`
- `greeting`
- `opening_hours`
- `payment_failed`
- `reset_password`
- `return_item`
- `talk_to_human`
- `track_order`

Reuse an existing intent when it fits. A new intent must be snake_case, describe what the speaker wants,
and be added to this list in the same change.

## Region format

`region` is a BCP 47-style tag: `es-` plus the ISO country code, e.g. `es-ES`, `es-MX`, `es-AR`, `es-CO`, `es-CL`.
Use `neutral` when the phrase has no regional marker. Label the region of the speaker, not of the topic.

## The `synthetic` field

- `true`: written or generated (by a model or by hand) rather than collected from real speech.
- `false`: genuinely collected from a real person, anonymized.
- Default is `false`, so always set it explicitly. When unsure, use `true`.

## Anonymization

Phrases must not contain real:
- names (people or small businesses),
- phone numbers,
- email addresses,
- street addresses,
- bank account, card or ID numbers.

Phrases with such data are not imported. Never replace them with a "similar" real value, and do not alter the
rest of the text beyond what is needed (see the golden rule). Generic words (`mi cuenta`, `mi pedido`) are fine.
