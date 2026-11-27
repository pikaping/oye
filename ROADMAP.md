# Oye · Roadmap

Un hito por semana. La semana empieza el lunes indicado.

## Fase 1 · Oye Corpus
- [x] 2026-11-30 · Repo: README con el lema, licencia Apache 2.0, CONTRIBUTING, estructura de carpetas
- [x] 2026-12-07 · Formato JSONL del corpus (frase, intención, región, rasgos) + primeras 100 frases
- [x] 2026-12-14 · Esquema de etiquetado + plantilla de issue para aportar frases
- [x] 2026-12-21 · Validador de formato y duplicados
- [x] 2026-12-28 · Validación del corpus en CI para cada PR
- [ ] 2027-01-04 · Controles de calidad en el validador (rasgo coloquial, un tercio con `typo`, "¿" opcional) + reescritura de frases sintéticas que no cumplan
- [ ] 2027-01-11 · Campo de región + 300 frases
- [ ] 2027-01-18 · Notebook: Oye Corpus contra un agente Dialogflow CX
- [ ] 2027-01-25 · Generador de variantes con Gemini (marcadas como sintéticas)
- [ ] 2027-02-01 · Guía y script de anonimización
- [ ] 2027-02-08 · Esquema v0.2 + documentación en inglés
- [ ] 2027-02-15 · Publicación en Hugging Face + tarjeta del dataset (requiere aprobación: cuenta de Hugging Face)
- [ ] 2027-02-22 · Release Oye Corpus v0.3

## Fase 2 · Oye Test
- [ ] 2027-03-01 · Paquete `oye`: CLI, estructura y tests
- [ ] 2027-03-08 · Conector Dialogflow CX
- [ ] 2027-03-15 · `oye test` ejecuta el corpus y guarda resultados
- [ ] 2027-03-22 · Informe de resultados en HTML
- [ ] 2027-03-29 · Conversaciones multiturno simuladas con Gemini
- [ ] 2027-04-05 · Tests de integración
- [ ] 2027-04-12 · Web de documentación + quickstart de 5 minutos
- [ ] 2027-04-19 · Mejoras a partir de issues abiertos
- [ ] 2027-04-26 · Conector genérico HTTP / Vertex AI
- [ ] 2027-05-03 · Plugin de Oye para Genkit (npm)
- [ ] 2027-05-10 · Acción de GitHub de Oye + evaluador LLM-as-judge
- [ ] 2027-05-17 · Good first issues + CONTRIBUTING en inglés
- [ ] 2027-05-24 · Release Oye Test 1.0 (PyPI y npm) (requiere aprobación: PyPI y npm)
- [ ] 2027-05-31 · Roadmap público actualizado

## Fase 3 · Oye Watch
- [ ] 2027-06-07 · Esqueleto de Oye Watch + formato de logs
- [ ] 2027-06-14 · Detector de bucles
- [ ] 2027-06-21 · Clasificador de frustración + anonimizador
- [ ] 2027-06-28 · Detector de derivación a humano
- [ ] 2027-07-05 · Importador desde BigQuery
- [ ] 2027-07-12 · Exportar frases fallidas a Oye Corpus
- [ ] 2027-07-19 · Informe semanal automático
- [ ] 2027-07-26 · Mejoras de rendimiento
- [ ] 2027-08-02 · Release Oye Watch 0.5
- [ ] 2027-08-09 · Corregir issues abiertos
- [ ] 2027-08-16 · Mejoras de documentación
- [ ] 2027-08-23 · Ampliar Oye Corpus con frases de Oye Watch
- [ ] 2027-08-30 · Release Oye Watch 1.0

## Fase 4 · Oye Starter
- [ ] 2027-09-06 · Plantilla con Agent Development Kit
- [ ] 2027-09-13 · Módulo de derivación a humano
- [ ] 2027-09-20 · Estrategias de fallback
- [ ] 2027-09-27 · Guía de estilo en el prompt del sistema
- [ ] 2027-10-04 · Integración Oye Test + ADK en CI
- [ ] 2027-10-11 · Despliegue en Cloud Run
- [ ] 2027-10-18 · Ejemplos: reservas, soporte, FAQ
- [ ] 2027-10-25 · Release Oye Starter 1.0
- [ ] 2027-11-01 · Rediseño de la web de documentación

## Fase 5 · Oye 1.0
- [ ] 2027-11-08 · Release conjunta Oye 1.0
- [ ] 2027-11-15 · Página de contribuidores
- [ ] 2027-11-22 · Roadmap 2028
- [ ] 2027-11-29 · Changelog anual
