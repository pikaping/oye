# Oye · Roadmap

Un hito por semana. La semana empieza el lunes indicado.

## Fase 1 · Oye Corpus
- [x] 2026-11-30 · Repo: README con el lema, licencia Apache 2.0, CONTRIBUTING, estructura de carpetas
- [x] 2026-12-07 · Formato JSONL del corpus (frase, intención, región, rasgos) + primeras 100 frases
- [x] 2026-12-14 · Esquema de etiquetado + plantilla de issue para aportar frases
- [x] 2026-12-21 · Validador de formato y duplicados
- [x] 2026-12-28 · Validación del corpus en CI para cada PR
- [ ] 2027-01-04 · Campo de región + 300 frases
- [ ] 2027-01-11 · Notebook: Oye Corpus contra un agente Dialogflow CX
- [ ] 2027-01-18 · Generador de variantes con Gemini (marcadas como sintéticas)
- [ ] 2027-01-25 · Guía y script de anonimización
- [ ] 2027-02-01 · Esquema v0.2 + documentación en inglés
- [ ] 2027-02-08 · Publicación en Hugging Face + tarjeta del dataset (requiere aprobación: cuenta de Hugging Face)
- [ ] 2027-02-15 · Release Oye Corpus v0.3

## Fase 2 · Oye Test
- [ ] 2027-02-22 · Paquete `oye`: CLI, estructura y tests
- [ ] 2027-03-01 · Conector Dialogflow CX
- [ ] 2027-03-08 · `oye test` ejecuta el corpus y guarda resultados
- [ ] 2027-03-15 · Informe de resultados en HTML
- [ ] 2027-03-22 · Conversaciones multiturno simuladas con Gemini
- [ ] 2027-03-29 · Tests de integración
- [ ] 2027-04-05 · Web de documentación + quickstart de 5 minutos
- [ ] 2027-04-12 · Mejoras a partir de issues abiertos
- [ ] 2027-04-19 · Conector genérico HTTP / Vertex AI
- [ ] 2027-04-26 · Plugin de Oye para Genkit (npm)
- [ ] 2027-05-03 · Acción de GitHub de Oye + evaluador LLM-as-judge
- [ ] 2027-05-10 · Good first issues + CONTRIBUTING en inglés
- [ ] 2027-05-17 · Release Oye Test 1.0 (PyPI y npm) (requiere aprobación: PyPI y npm)
- [ ] 2027-05-24 · Roadmap público actualizado

## Fase 3 · Oye Watch
- [ ] 2027-05-31 · Esqueleto de Oye Watch + formato de logs
- [ ] 2027-06-07 · Detector de bucles
- [ ] 2027-06-14 · Clasificador de frustración + anonimizador
- [ ] 2027-06-21 · Detector de derivación a humano
- [ ] 2027-06-28 · Importador desde BigQuery
- [ ] 2027-07-05 · Exportar frases fallidas a Oye Corpus
- [ ] 2027-07-12 · Informe semanal automático
- [ ] 2027-07-19 · Mejoras de rendimiento
- [ ] 2027-07-26 · Release Oye Watch 0.5
- [ ] 2027-08-02 · Corregir issues abiertos
- [ ] 2027-08-09 · Mejoras de documentación
- [ ] 2027-08-16 · Ampliar Oye Corpus con frases de Oye Watch
- [ ] 2027-08-23 · Release Oye Watch 1.0

## Fase 4 · Oye Starter
- [ ] 2027-08-30 · Plantilla con Agent Development Kit
- [ ] 2027-09-06 · Módulo de derivación a humano
- [ ] 2027-09-13 · Estrategias de fallback
- [ ] 2027-09-20 · Guía de estilo en el prompt del sistema
- [ ] 2027-09-27 · Integración Oye Test + ADK en CI
- [ ] 2027-10-04 · Despliegue en Cloud Run
- [ ] 2027-10-11 · Ejemplos: reservas, soporte, FAQ
- [ ] 2027-10-18 · Release Oye Starter 1.0
- [ ] 2027-10-25 · Rediseño de la web de documentación

## Fase 5 · Oye 1.0
- [ ] 2027-11-01 · Release conjunta Oye 1.0
- [ ] 2027-11-08 · Página de contribuidores
- [ ] 2027-11-15 · Roadmap 2028
- [ ] 2027-11-22 · Changelog anual
