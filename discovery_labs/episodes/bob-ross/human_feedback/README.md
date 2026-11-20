# AI Discovery Labs · Bob Ross — índice de Human Feedback

> **Estado del 19 de noviembre de 2026:** HF-00/HF-01 preparados retrospectivamente y HF-02 para revisión actual, todos **DRAFT / decisión PENDING**. HF-03/HF-04: **NO ejecutados**. No se infiere aprobación humana ni `RESEARCH_APPROVED:<commit>`.

El protocolo se fusionó en PR #17 mientras la investigación ya se ejecutaba con la base anterior. [Transición documentada](../research/PROTOCOL_TRANSITION.md). Los cálculos O2 previos se conservan; su promoción editorial está retenida hasta HF-02. Las versiones se prepararon con evidencia real y siguen DRAFT por QA visual pendiente.

**Protocolo obligatorio:** [HUMAN_FEEDBACK_CHECKPOINTS.md](../entry_pack/HUMAN_FEEDBACK_CHECKPOINTS.md). Plantillas compartidas: `discovery_labs/shared/templates/HUMAN_FEEDBACK_CHECKPOINT_TEMPLATE.md`, `HUMAN_FEEDBACK_REPORT_TEMPLATE.html` y `HUMAN_FEEDBACK_CHECKPOINT_SCHEMA.json`.

| ID | Disparador de publicación del primer reporte | Informe más reciente | Estado humano |
|---|---|---|---|
| **HF-00 — Brújula** | Auditoría y conciliación ya ejecutadas; paquete retrospectivo | [v01 · informe](HF-00/v01/report.html) | `PENDING` |
| **HF-01 — Descubrimientos O1** | Tres O1 y replicación; paquete retrospectivo | [v01 · informe](HF-01/v01/report.html) | `PENDING` |
| **HF-02 — Priorización O2** | DR-05a y controles previos; revisión humana actual | [v01 · informe](HF-02/v01/report.html) | `PENDING` |
| **HF-03 — Robustez** | O2/O3 pertinentes + DR-04 con controles adversariales | Aún no existe | `NOT_STARTED` |
| **HF-04 — Aprobación F1** | DR-05b, HTML científico + pruebas y QA | Aún no existe | `NOT_STARTED` |

### Qué debe ocurrir con cada publicación

Crear carpeta **nueva** `HF-XX/v01/` (o `v02` para una revisión), con:
- `report.html`: **Resumen ejecutivo en primera pantalla**, antes de gráficas; «qué aprendimos», «qué cambió», sorpresa validada o negativa explícita, sugerencia y limitación.
- `feedback.md`: hasta tres preguntas para la persona, recomendación y su respuesta **si la proporciona**.
- `checkpoint.json`: evidencia, estado y decisión según schema; `PENDING` por defecto.
- `charts/` y `data/`: figuras y derivados originales con fuente, muestra, denominador, incertidumbre, código y derechos.
- Actualizar este índice con enlace a la **última versión**, versión previa, cambios principales y decisión registrada, sin eliminar reportes anteriores.

**No publicar gráficas ficticias** ni «insights» imaginados. HF-00 puede enseñar gráficas de cobertura y calidad si sus conteos se comprobaron; HF-01…HF-04 necesitarán resultados científicos reales para visualizaciones de descubrimiento.
