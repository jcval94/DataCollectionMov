# PROMPT PARA CODEX / CLAUDE CODE — AI DISCOVERY LABS: FASE 0

Actúa como investigador principal, historiador documental, revisor metodológico, periodista de datos, curador de recursos visuales y científico de datos.

**Objetivo:** convertir el episodio de Bob Ross en un paquete profundo y revisable de investigación antes de redactar su HTML definitivo. Este es un trabajo de investigación y planificación CIENTÍFICA, no un encargo de producir video.

## Repositorio y restricciones

Repo: https://github.com/jcval94/DataCollectionMov
PR y rama existente: https://github.com/jcval94/DataCollectionMov/pull/5
Directorio permitido de escritura: `discovery_labs/episodes/bob-ross/`. No cambiar nada fuera; no sobrescribir trabajo local sin guardar, no fusiones automáticamente.

Primero comprueba branch, working tree, archivos y fuentes. Usa los datos originales `data/elements-by-episode.csv` con su hash; no reemplaces los 403 episodios por las 12 filas de muestra.

## Acciones obligatorias, en este orden

1. Lee íntegramente `intake/README.md`, `intake/DEEP_RESEARCH_MASTER.md`, `intake/PLAN_DE_INVESTIGACION.md`, `intake/QUESTION_GRAPH.md`, `intake/metadata.json` y la skill `intake/skills/research-question-architect/SKILL.md`.
2. Ejecuta los cinco prompts de `intake/prompts/` haciendo Deep Research real sobre historia, producción, contexto, investigaciones anteriores, mapeo de pinturas/derechos y síntesis.
3. Construye una **biografía científica verificable** y una cronología de la serie 1983–1994. Separa emisión, grabación y creación. No afirmes que la enfermedad causó un cambio de estilo sin fechas y método suficientes.
4. Crea un ledger de evidencia con fuentes y contradicciones, indicando lo verificado, lo desconocido, lo retrospectivo y lo no identificable.
5. Reproduce desde los 403 registros los principales perfiles por temporada, por episodio y por era. Busca outliers multiescala, cambios persistentes, coocurrencias raras y sensibilidad a invitado, métricas y etiquetas.
6. Activa la skill de investigación y transforma los 12 arcos en **investigaciones rigurosas de Q1 + dos Q2 + Q3**. Rechaza preguntas que sean solo una query. Asegura que cada pregunta tenga utilidad humana, falsadores, método y visualización.
7. Diseña 7 visualizaciones editoriales impresionantes **pero fieles a la evidencia**; prueba hover/focus/tap para los puntos de los clusters con imágenes reales **únicamente si se verifica permiso**. De lo contrario usar tooltip de texto y enlace al sitio de origen.
8. Puntúa las 12 propuestas con la rúbrica y selecciona hasta tres arcos piloto listos para ejecutar y el resto con blockers.
9. Completa el material del paquete: nueva evidencia, experimentos preliminares, cronología, derechos y versión priorizada de preguntas. Conserva procedencia y scripts reproducibles.
10. Termina con informe claro, archivos modificados, pruebas ejecutadas, hallazgos, bloqueos, PR y próximos pasos. Mantén approval_status=PENDIENTE_DE_APROBACION.

## Calidad

- No inventar narrativas dramáticas ni resultados «sorprendentes».
- Diferenciar hipótesis de hallazgos comprobados.
- Explicar n/N, denominadores y niveles episodio/temporada/era.
- Corregir múltiples comparaciones y separar outliers genuinos de errores.
- No inferir estados anímicos, personalidad, enfermedad o causalidad a partir de arte.
- Respetar derechos de imagen, audio y nombre.
- Priorizar 3 investigaciones excelentes sobre 12 seudodescubrimientos.

**NO CREAR `research_guide.html`, guion audiovisual, storyboard, intro, Remotion ni MP4 en esta ejecución.** Esta es solo la Fase 0. En otra ejecución autorizada se construirá el informe científico HTML (Fase 1). El segundo HTML y el video seguirán bloqueados hasta las aprobaciones correspondientes.

Empieza ahora por la auditoría de los recursos de entrada y el Deep Research 01. No te detengas en un listado de ideas: entrega investigación con fuentes y artefactos auditables.
