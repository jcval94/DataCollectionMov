# AI Discovery Labs · Bob Ross — índice de Human Feedback

> **Estado del 19 de noviembre de 2026:** checkpoints **DISEÑADOS, aún NO ejecutados**. Ningún informe con resultados científicos, aprobación de O2 ni `RESEARCH_APPROVED:<commit>` se infiere de este documento.

**Protocolo obligatorio:** [HUMAN_FEEDBACK_CHECKPOINTS.md](../entry_pack/HUMAN_FEEDBACK_CHECKPOINTS.md). Plantillas compartidas: `discovery_labs/shared/templates/HUMAN_FEEDBACK_CHECKPOINT_TEMPLATE.md`, `HUMAN_FEEDBACK_REPORT_TEMPLATE.html` y `HUMAN_FEEDBACK_CHECKPOINT_SCHEMA.json`.

| ID | Disparador de publicación del primer reporte | Informe más reciente | Estado humano |
|---|---|---|---|
| **HF-00 — Brújula** | QA real de datos/fuentes y conciliación DR ↔ BR/H | Aún no existe | `NOT_STARTED` |
| **HF-01 — Descubrimientos O1** | Al menos 1–2 O1 ejecutadas y reproducidas | Aún no existe | `NOT_STARTED` |
| **HF-02 — Priorización O2** | DR-05a con O1 medidas y fuentes conciliadas | Aún no existe | `NOT_STARTED` |
| **HF-03 — Robustez** | O2/O3 pertinentes + DR-04 con controles adversariales | Aún no existe | `NOT_STARTED` |
| **HF-04 — Aprobación F1** | DR-05b, HTML científico + pruebas y QA | Aún no existe | `NOT_STARTED` |

**Quality gate obligatorio para publicación:** `python discovery_labs/shared/validators/validate_human_feedback.py --checkpoint discovery_labs/episodes/bob-ross/human_feedback/HF-XX/vNN --ready`. Solo aplicable **cuando exista un informe real**. La validación estructural complementa —no reemplaza— la revisión de métodos, resultados y derechos. El primer reporte HF-00 sigue pendiente de auditar el dataset.

### Investigación en rama no aprobada

El [PR #18](https://github.com/jcval94/DataCollectionMov/pull/18) (borrador, no integrado en `main` cuando se registró) contiene los **primeros informes reales HF-00/HF-01/HF-02** con resultados y gráficas, pero su estado es `DRAFT/PENDING` y les faltaba QA visual certificada. Este índice describe lo que existe **en main**, de ahí la columna «Aún no existe». Consultar su handoff antes de rehacer análisis o solicitar una aprobación. No marcarlo `APPROVED` por ser reproducible o tener CI verde.

### Qué debe ocurrir con cada publicación

Crear carpeta **nueva** `HF-XX/v01/` (o `v02` para una revisión), con:
- `report.html`: **Resumen ejecutivo en primera pantalla**, antes de gráficas; «qué aprendimos», «qué cambió», sorpresa validada o negativa explícita, sugerencia y limitación.
- `feedback.md`: hasta tres preguntas para la persona, recomendación y su respuesta **si la proporciona**.
- `checkpoint.json`: evidencia, estado y decisión según schema; `PENDING` por defecto.
- `charts/` y `data/`: figuras y derivados originales con fuente, muestra, denominador, incertidumbre, código y derechos.
- Actualizar este índice con enlace a la **última versión**, versión previa, cambios principales y decisión registrada, sin eliminar reportes anteriores.

**No publicar gráficas ficticias** ni «insights» imaginados. HF-00 puede enseñar gráficas de cobertura y calidad si sus conteos se comprobaron; HF-01…HF-04 necesitarán resultados científicos reales para visualizaciones de descubrimiento.
