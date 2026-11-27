# Notes

## Ideas

- oye-0054 might need the `typo` feature.
- Datos de estilo real (chat de ~62.000 mensajes): solo el 1 % de las preguntas lleva "¿"; ~80 % empieza en mayúscula por el autocorrector; mediana de 6 palabras. Ajustar las reglas de calidad del corpus: la falta de "¿" es la norma, las minúsculas iniciales no.
- `normalize_text` treats ñ as n (e.g. `año` vs `ano`), which may cause near-duplicate false positives.
- Add corpus quality checks to the validator (e.g. at least one third of a batch carries `typo`).

## Pendiente del autor

- Mover `ci/ISSUE_TEMPLATE/` a `.github/ISSUE_TEMPLATE/`.
- Mover `ci/corpus-validate.yml` a `.github/workflows/`.
