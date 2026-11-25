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
- No modifiques `.github/`, `.claude/`, `scripts/`, `LICENSE` ni este archivo.
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
posts/         Plan y borradores de LinkedIn (los escribe el writer; los publica oye-linkedin.yml)
scripts/       Publicación en LinkedIn
```

## Sesión diaria (orquestación)

La sesión la dirige el orquestador, que delega en los subagentes de `.claude/agents/`.
El orquestador no escribe código: coordina, decide y es el único que hace commits y push.
Los subagentes se lanzan siempre en primer plano, uno detrás de otro, esperando su resultado: la sesión no es interactiva y, si el orquestador termina su turno, todo lo que siga en marcha se cancela.

1. **planner** → devuelve 3-5 tareas para el hito activo: el primer hito sin marcar de ROADMAP.md, sea cual sea su fecha.
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
5. `git push` a main.

Si ninguna tarea llega a commit, no hagas push de nada salvo el diario explicando por qué.
