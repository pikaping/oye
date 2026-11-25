# Oye

Test your agents with how people actually talk.

Oye es un kit open source para probar agentes conversacionales con lenguaje real:
- **Oye Corpus**: dataset de español coloquial (JSONL).
- **Oye Test**: probador por línea de comandos, con plugin para Genkit.
- **Oye Watch**: análisis de conversaciones en producción.
- **Oye Starter**: plantilla de agente con el Agent Development Kit (ADK).

## Reglas de trabajo

- Python 3.12, tipado, `pytest` para tests. El plugin de Genkit va en TypeScript dentro de `plugins/genkit/`.
- Commits pequeños con Conventional Commits en inglés: `feat(test): ...`, `fix(corpus): ...`, `docs: ...`.
- Cada commit deja los tests en verde. Si algo no se puede terminar hoy, deja un commit coherente y una nota en `NOTES.md`.
- Código, docstrings y documentación en inglés. Los datos del corpus, en español.
- Nunca subas claves, tokens ni datos personales. Las frases del corpus van anonimizadas.
- Nada de commits de relleno: si el hito está atascado, mejora tests o documentación del hito actual.
- No modifiques `.github/`, `.claude/`, `scripts/`, `LICENSE`, `VISION.md` ni este archivo.
- Ejecuta siempre los tests con `pytest` a secas (no `python -m pytest`), que es como los ejecuta el orquestador antes de cada commit.
- Si al construir o revisar descubres algo que falta pero no es de la tarea actual, anótalo en `NOTES.md`, sección "Ideas", en una línea. El strategist lo convertirá en hito si merece la pena.
- No publiques nada en LinkedIn ni en ningún otro sitio: eso lo hace solo el workflow de LinkedIn.

## Estructura

```
corpus/        Oye Corpus (data/*.jsonl, schema, validador)
oye/           paquete Python (CLI `oye`)
  test/        Oye Test
  watch/       Oye Watch
plugins/genkit Plugin de Oye para Genkit
starter/       Oye Starter (plantilla ADK)
tests/
docs/
journal/       Diario de cada sesión (lo escribe el chronicler)
VISION.md      Brújula del proyecto (solo la edita el autor)
NOTES.md       Ideas y deuda técnica que van apareciendo
posts/         Plan y borradores de LinkedIn (los escribe el writer; los publica oye-linkedin.yml)
scripts/       Publicación en LinkedIn
```

## Sesión diaria (orquestación)

La sesión la dirige el orquestador, que delega en los subagentes de `.claude/agents/`.
El orquestador no escribe código: coordina, decide y es el único que hace commits y push.
Los subagentes se lanzan siempre en primer plano, uno detrás de otro, esperando su resultado: la sesión no es interactiva y, si el orquestador termina su turno, todo lo que siga en marcha se cancela.

1. **planner** → devuelve 3-5 tareas para el hito activo: el primer hito sin marcar de ROADMAP.md, sea cual sea su fecha, saltándose los marcados `(requiere aprobación: ...)`.
   Si el hito activo se completa y queda tiempo, sigue con el siguiente en la misma sesión (máximo 8 commits al día).
2. Para cada tarea, en orden:
   1. **builder** implementa la tarea.
   2. **tester** añade tests y ejecuta `pytest`.
      Si devuelve ROJO, vuelve al builder con el fallo (máximo 2 intentos).
   3. **reviewer** revisa el diff.
      Si pide CAMBIOS, vuelve al builder con la lista (máximo 2 intentos).
   4. Con VERDE y APROBADO, el orquestador hace commit con el mensaje propuesto por el planner.
   5. Si tras los intentos la tarea sigue sin pasar, descarta sus cambios con `git restore .` y `git clean -fd` (solo archivos sin seguimiento de esa tarea), anótalo en `NOTES.md` y pasa a la siguiente.
3. Si el hito queda completo, marca [x] en ROADMAP.md en el último commit.
4. **chronicler** escribe el diario del día; el orquestador lo añade en un commit `docs(journal): ...`.
   Si hoy es lunes, **writer** redacta además el post del martes en `posts/`, y el orquestador lo añade en un commit `docs(posts): ...`.
   Si hoy es viernes (`date +%u` = 5) o quedan menos de 5 hitos sin marcar, **strategist** revisa el roadmap,
   y el orquestador añade sus cambios en un commit `docs(roadmap): ...`.
5. `git push` a main.

Si ninguna tarea llega a commit, no hagas push de nada salvo el diario explicando por qué.

## Calidad del corpus

- Toda frase sintética lleva al menos un rasgo coloquial. Nada de frases correctas y completas como "Buenos días, ¿qué tal?".
- Al menos un tercio de cada lote lleva `typo`: tildes omitidas, letras cambiadas, sin mayúsculas, sin signos de apertura.
- Antes de añadir un lote, el reviewer descarta cualquier frase que podría salir de un manual de atención al cliente.
- Las frases sintéticas existentes que no cumplan esto se reescriben o se eliminan en el siguiente hito del corpus.

## Integraciones externas

- Las integraciones (Dialogflow CX, Vertex AI, Gemini, BigQuery, Genkit, ADK, Cloud Run) se desarrollan sin credenciales:
  una interfaz común, una implementación real con el SDK oficial y una implementación falsa para los tests.
- Los SDKs van como dependencias opcionales (extras en pyproject.toml, por ejemplo `oye[dialogflow]`), nunca obligatorias.
- `pytest` nunca necesita credenciales ni red: los tests de la implementación real usan mocks del SDK.
- La implementación real solo se activa si su credencial existe en el entorno. Si no existe, falla con un error que explica qué configurar.
- Ninguna sesión diaria llama a servicios reales ni publica nada: ni Hugging Face, ni PyPI, ni npm, ni despliegues.
  El paso final se anota en `NOTES.md`, sección "Pendiente del autor", con las instrucciones exactas.
- Cada integración documenta en `docs/` cómo configurarla. Para los costes, enlaza a la página oficial de precios; nunca inventes cifras.
- Los hitos marcados `(requiere aprobación: ...)` no se trabajan. Solo el autor puede quitar esa marca.
