# Prompt para nueva conversación — AI Discovery Labs / Bob Ross (19 nov 2026)

> Copiar **desde «MISIÓN» hasta «SALIDA»** en un chat nuevo (idealmente en Work con GitHub conectado). Leer primero [HANDOFF_2026-11-19.md](HANDOFF_2026-11-19.md) y contrastar cada afirmación con el estado real de `main`. Este prompt arranca por la **auditoría y conciliación científica**, no por generar un video ni fingir investigaciones ejecutadas.

---

## MISIÓN

Actúa como un equipo científico/técnico de clase mundial: Principal Data Scientist, estadístico investigador, Data Engineer, historiador de medios, especialista de ciencia abierta y derechos, MLOps, visualización científica y diseñador instruccional.

Trabaja DIRECTAMENTE en https://github.com/jcval94/DataCollectionMov, episodio `discovery_labs/episodes/bob-ross/`. Mi objetivo con AI Discovery Labs es **descubrir insights increíbles, originales y científicamente defendibles de cada dataset** y convertirlos en laboratorios reproducibles de ~45 minutos. Cada pregunta/resultado debe responder **CÓMO, POR QUÉ y PARA QUÉ**, considerando modelos, contraste estadístico distinto, rivales, incertidumbre y utilidad.

**No solicites otra vez las tres investigaciones:** Ya te compartí DR-01 (biografía), DR-02 (datos/multisource) y DR-03 (mitos/antecedentes/hipótesis). Están archivadas en `entry_pack/research_received/` y explicadas en el handoff. Son **versiones estructuradas no literales**, NO investigaciones validadas, y no constituyen evidencia de que O1 haya sido medida.

## 0. LECTURA Y ESTADO INICIAL OBLIGATORIOS

1. Lee `entry_pack/HANDOFF_2026-11-19.md`, `entry_pack/START_HERE_NEW_CHAT.md`, `entry_pack/RESEARCH_PLAN.md`, `entry_pack/research_received/README.md` y `MANIFEST.json`.
2. Lee `shared/skills/question-forge/SKILL.md`, `shared/templates/ENTRY_PACK_TEMPLATE.md`, `shared/templates/DEEP_RESEARCH_TEMPLATE.md`, `shared/model_catalog/MODEL_SET.md`, `entry_pack/QUESTIONS_MASTER.md`, `questions_master.json`, `DEEP_RESEARCH_PROMPTS.md`, `QA_PACK_STATUS.md`, y revisa `research_guide.html` (V3).
3. Verifica en GitHub el estado actualizado de los PR: #12, #14, #15 ya se fusionaron el 19-11-2026. Evita modificaciones en PR históricos. Otros PR abiertos #2/#4/#6/#7 trataban lotes diferentes: **no fusionarlos sin auditarlos y sin que pertenezcan a esta tarea**.
4. Lee el dataset REAL y los scripts/tests de Bob Ross. No confundas claims del DR con observaciones verificadas. Haz inventario de conflictos, de cosas ejecutadas, de cosas planificadas y de los permisos/derechos disponibles.
5. Si no puedes entrar a algún recurso, declara exactamente el bloqueo y continúa con evidencias accesibles; **no suplas datos faltantes mediante imaginación**.

### Antes de repetir experimentos: revisar el PR #18 en borrador

Existe trabajo científico nuevo y aún **no fusionado**: [PR #18](https://github.com/jcval94/DataCollectionMov/pull/18), rama `research/bob-ross-o1-20261119`. Incluye investigación O1 reproducible, guía V4 e informes HF-00/HF-01/HF-02 en estado DRAFT/PENDING, además de `entry_pack/HANDOFF_2026-11-19_SCIENTIFIC_O1.md`.

**Comprueba su estado actual**, lee `research/README.md`, `SOURCE_REVIEW.md`, `PROTOCOL.md`, `QA.md` y HF-02. El CI del commit `b4deda1b268149acdabd6fbb67608e9ca015cd94` era success, pero no existían certificación visual ni aprobación humana. **No repetir O1 sin verificar estos artefactos ni fusionar PR #18 saltando HF-02.** Si la situación cambió, documenta el cambio de estado con commits. Si permanece pendiente, concentra la siguiente conversación en revisar evidencias, preguntas HF-02 y accesibilidad visual para decidir si promover o no los hallazgos.

## 1. ANALIZAR PRIMERO, EDITAR DESPUÉS

Entrega primero un diagnóstico y matriz de conciliación (con fuente/ruta y nivel de confianza). Inspecciona al menos:

- 403 episodios, 69 columnas y 67 etiquetas; SHA-256 del CSV original (referencia a contrastar `42045c8b8aaa8296095d6b294927fb9d0f73a57259f59b560c375844c0fe01cf`), IDs, tipos, ausencias, duplicados.
- Reconciliación de las **3,221, 3,224 y 3,324** marcas positivas reportadas por diferentes fuentes.
- Autoría: **381 Bob / 22 invitados**, otras listas contradictorias; tres episodios declarados incompletos en la viñeta R; `LAKESIDE CABIN` duplicado como título.
- Qué variables reales existen. No inventes columnas `PERSON` o `CHIMNEY`; comprueba etiquetas estructurales, de marco, de paisaje y de invitado; jerarquías CLOUDS/CIRRUS/CUMULUS, FRAMED/subtipos.
- Distinción **fecha de grabación vs primera emisión vs repetición vs publicación digital**. No inferir efecto de duelo, linfoma, product placement ni estudio de 1988 sin identificación válida.
- Versiones de pinturas **Kowalski/tv/book** y derechos de reproducciones. CSV con licencia abierta NO habilita automáticamente imágenes, video, voz ni transcripciones.
- Evidencia de DR-01/02/03 con conflictos y URLs; fuentes adicionales jwilber, BobRossColors, fivethirtyeightdata, TidyTuesday, Wikipedia, OpenBrush/WikiArt: evaluar datos, licencia, llaves y cobertura efectiva.

## 2. CONCILIAR PREGUNTAS Y ELEGIR INVESTIGACIONES

No crear un segundo banco. Cruza las **14 investigaciones canónicas BR** con las **10 hipótesis H1–H10** de DR-03, las oportunidades de DR-01/02 y antecedentes. Para cada investigación registra:

`canonical_id, source_DR, claim_ids, O1, dataset_version, grain, denominator, prerequisites, candidate_model, separate_statistical_test, hypotheses, rivals, evidence_status, required_rights, feasibility, novelty, surprise, pedagogical_value, next_action`.

Selecciona **3–5 arcos prioritarios** con rubrica explícita; no «aprobar» todas las preguntas ni prometer impacto extraordinario. Considera primero O1 con bajos bloqueos, como **H8 programación secuencial**; evalúa robustez de clustering **H6** con matriz auditada; **H1** solo después de verificar paletas. **H5 y H7 requieren revisar derechos y acceso a imágenes**; no asumas disponibilidad plena pese al ranking previo.

Para cada arco explica **CÓMO se medirá, POR QUÉ tiene tensión real e hipótesis rival, PARA QUÉ enseñará o permitirá descubrir algo**. Distingue preguntas falsables de afirmaciones históricas no medibles.

## 3. EJECUTAR INVESTIGACIÓN O1 REPRODUCIBLE (EN UN SEGUNDO LOTE)

Una vez superado el QA de datos y hecha la priorización, implementa **solo los O1 técnicamente factibles**, en una rama específica con scripts, pruebas, snapshots/manifiestos de origen y resultados estructurados. Ejecuta modelos adecuados del catálogo y **un contraste estadístico formal distinto**, con baseline, incertidumbre, controles, análisis negativos, out-of-sample cuando aplique y QA adversarial.

**Importante:** nunca inventes resultados. Si la ejecución requiere permiso/datos no disponibles, marca BLOCKED y deja diseño reproducible y criterio de desbloqueo.

Separa claramente:
- `PLAN_ONLY`: diseño sin ejecutar.
- `EXECUTED`: cálculo guardado, reproducible, verificable.
- `REFUTED / INCONCLUSIVE`: datos no apoyan o no alcanzan.
- `APPROVED`: únicamente con aprobación humana pertinente.

## 4. HTML Y DEEP RESEARCH ESCALONADOS

Seguir metodología incorporada en #14:

**DR-01/02/03** ya recibidos, pero sus afirmaciones requieren triangulación y comprobación. **NO lanzar automáticamente DR-04 profundo ni DR-05b final**.

El HTML científico debe abrir con un **párrafo de contexto general**, misión, cobertura y límites, **un solo índice de O1**, métodos/figuras/sources, resultados/contradicciones, utilidad y reproducción. No mostrar O2 ni O3 como preguntas activas desde el comienzo. Las futuras **O2 solo aparecen después de O1 medidas + Deep Research temprano verificado + DR-05a de síntesis adversarial**; O3 requiere O2 ejecutada y rival comprobable. Registrar `parent_id`, `trigger_evidence`, versión/commit, fuentes, resultados nulos y cambios.

**No crear guion, voz, storyboard, Remotion ni video.** El paso Fase 1→2 requiere aprobación explícita de la versión/commit científico, y Fase 2→3 otra aprobación. El hecho de fusionar un PR no equivale a aprobación científica.

## 4 bis. HUMAN FEEDBACK OBLIGATORIO · INFORMES VISUALES

Lee `entry_pack/HUMAN_FEEDBACK_CHECKPOINTS.md`, `discovery_labs/shared/templates/HUMAN_FEEDBACK_CHECKPOINT_TEMPLATE.md`, su schema JSON y la plantilla `HUMAN_FEEDBACK_REPORT_TEMPLATE.html`.

Además de las fases científicas, produce **informes humanos versionados** en `discovery_labs/episodes/bob-ross/human_feedback/HF-XX/vNN/`:

- **HF-00:** después de auditar/conciliar el CSV y DR, antes de priorizar 3–5 arcos O1.
- **HF-01:** después de los primeros O1 calculados y reproducidos.
- **HF-02:** después de DR-05a, para decidir explícitamente qué O2 se investiga.
- **HF-03:** después de O2/O3 y DR-04, para sensibilidad, rivales y seleccionar insights defendibles.
- **HF-04:** después de DR-05b, QA y guía científica completa, para mi aprobación del commit exacto.

**EL REQUISITO MÁS IMPORTANTE ES LA PRIMERA PANTALLA:** título y breve fecha, seguidos INMEDIATAMENTE por un **Resumen ejecutivo claro** con lo que aprendimos, qué avanzó vs la versión previa, un insight sorprendente **solo si es reproducible**, tu recomendación y una limitación principal. Después una sección «qué cambió», y **2–4 gráficas muy buenas si hay datos verificados**: figura central, contraste robusto, figura adversarial, e inspector por episodio si sirve. Cada gráfico debe tener n/denominador, baseline, incertidumbre, fuente, código, derechos, alt text y QA móvil/escritorio/teclado. No rellenar números ni dibujos fingiendo descubrimientos.

Incluye CÓMO / POR QUÉ / PARA QUÉ, **máximo tres preguntas para mí** con opciones, recomendación y consecuencias de posponer, más próximos pasos. Guarda `report.html`, `feedback.md`, `checkpoint.json`, charts y datos derivados legalmente utilizables; una revisión v2 agrega versión, no sobrescribe la anterior.

**HF-02 y HF-04 son gates humanos de decisión.** No tomar el silencio como aprobación, no promover O2 ni ir a storyboard por ausencia de respuesta. Si los hallazgos son inconclusos, el resumen debe comunicarlo honestamente; la ausencia de patrón también es aprendizaje.

## 4 ter. PUERTA AUTOMÁTICA PARA INFORMES HUMANOS

Antes de entregar **cada reporte real** HF-00…HF-04, ejecuta:

```bash
python discovery_labs/shared/validators/validate_human_feedback.py \
  --checkpoint discovery_labs/episodes/bob-ross/human_feedback/HF-XX/vNN --ready
```

Debe pasar el contrato de `checkpoint.json` (incluido `report_starts_with_summary: true`), `feedback.md`, `report.html` sin placeholders sin sustituir, gráfica(s) realmente generadas con evidencias, validaciones visuales completas, máximo tres preguntas y aprobación explícita cuando corresponda. Si falla, **no** declares el checkpoint listo ni uses el reporte para activar O2 o pasar al audiovisual. **PASS estructural ≠ resultado científico verificado**: además contrasta resultados numéricos contra su fuente y prueba adversarial. Si todavía es borrador sin resultados, omite `--ready` y marca `DRAFT/BLOCKED`; nunca generes cifras de ejemplo como si fueran hallazgos.

## 5. CÓDIGO, GIT Y VALIDACIÓN

- Mantener cambios dentro de `discovery_labs/episodes/bob-ross/` excepto mejoras realmente generalizables acordadas en `discovery_labs/shared/`, en PR separado.
- No borrar ni reescribir `research_received/` ni los originales. No hacer reset destructivo ni sustituir un banco editorial con otro.
- Trabajar sobre rama nueva, pruebas reproducibles y PR legible. No mezclar investigación, cambios de datos y decisiones audiovisuales en un solo PR.
- Ejecutar tests de Bob Ross/validadores compartidos, y documentar las comprobaciones reales (incluidos fallos). Verificar conflictos/CI antes de fusionar.
- Guardar toda evidencia/decisión/resultado en el repo de forma trazable, actualizar `HANDOFF_2026-11-19.md` o crear sucesor por fecha, y mantener el prompt de continuidad.
- Si una decisión científica tiene consecuencias importantes, documentar alternativas y solicítame aprobación antes de promoción a `APPROVED`.

## SALIDA

En esta nueva conversación quiero:

1. Diagnóstico factual de lo que **hay, funciona, falta o es dudoso** en el repo.
2. Matriz reconciliada DR-01/02/03 ↔ BR-01…BR-14 ↔ H1…H10 y un plan científico de 3–5 arcos con CÓMO/POR QUÉ/PARA QUÉ.
3. Auditoría del CSV, versiones y fuentes; resultados de QA **realmente ejecutado**.
4. Implementación de los primeros O1 viables si el dato y los permisos están listos; de lo contrario, PR de evidencias y bloqueos verificables, no promesas.
5. Enlaces a PR, commits, QA y handoff actualizado, además de un resumen concreto de qué sigue.

La prioridad absoluta es **descubrir hechos reales sorprendentes y rigorosos**, no producir un HTML bonito o más documentos sin contrastar datos. Primero análisis, luego implementación, y finalmente narración científica basada en resultados.
