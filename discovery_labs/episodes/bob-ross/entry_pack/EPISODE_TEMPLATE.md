# Plantilla reutilizable del Paquete de Entrada — cualquier episodio AI Discovery Labs

> **Copia heredada/compatibilidad.** La plantilla central para otros episodios ahora se desarrolla en [discovery_labs/shared/templates/ENTRY_PACK_TEMPLATE.md](https://github.com/jcval94/DataCollectionMov/blob/feat/discovery-labs-shared-research-core/discovery_labs/shared/templates/ENTRY_PACK_TEMPLATE.md) (PR #11, pendiente). **NO copies la skill ni el catálogo de modelos** desde esta plantilla antigua. Conservar hasta integración y actualización de referencias.


> Copiar/adaptar este contrato a cada nuevo dataset. La skill `skills/question-forge/SKILL.md` lo consume. **No** construir guion ni video antes de aprobar el primer HTML.

## 0. Identidad del caso
- `episode_id`, slug, título provisional (sin revelar resultado), macrocategoría y audiencia.
- El problema humano: ¿qué historia, tensión, contradicción o decisión real vuelve interesantes los datos?
- Definición clara de unidad de observación, cobertura y periodo.
- Personas/organizaciones y derechos de imagen: no inferir hechos personales sensibles a partir de datos indirectos.

## 1. Carpeta mínima
```text
episode_slug/
  entry_pack/
    START_HERE_NEW_CHAT.md         # Contexto autocontenido y estado de aprobación
    README.md                      # Índice y orden de lectura
    metadata.json                  # Grano, cobertura, licencia, procedencia, hashes
    sample_raw.csv                 # 10–20 filas verdaderas con muestreo diverso
    sample_features.csv            # Mismo subset, transformaciones rotuladas
    DEEP_RESEARCH_PROMPTS.md       # 3–5 ejes independientes + síntesis
    CONTEXT_CLAIMS.md              # Fuente, afirmación, fecha, confianza, contradicciones
    RESEARCH_PLAN.md               # Lotes, dependencias, reglas, QA y gates
    MODEL_SET.md                   # Menú de modelos por tarea, adecuación y restricciones
    QUESTIONS_MASTER.md            # ÚNICA sección editorial de investigaciones
    questions_master.json          # Versión estructurada que alimenta el HTML
    VISUAL_DESIGN.md               # Argumentos visuales, QA y derechos
    skills/question-forge/SKILL.md # Skill generalizable
    PROMPT_FASE1_V2.md             # Prompt portátil para preparar guía científica
  research_guide.html              # ÚNICA guía de Fase 1, tras investigar
```

## 2. Los cinco Deep Research mínimos
**DR-A Historia y dominio:** qué pasó antes/durante/después, contexto político/económico/cultural/biográfico relevante, fechas corroboradas, fuentes primarias y secundarias, sesgos de la literatura.

**DR-B Datos y accesos:** origen, cobertura, formatos, tamaño, licencias, perfiles, problemas de muestreo, frecuencia, cambios de esquema, joins, calidad y fechas de observación.

**DR-C Mitos y antecedentes:** afirmaciones documentadas, quién las dijo, contraejemplos, análisis similares, patrones aceptados o discutidos. No inventar una creencia.

**DR-D Visualización, imágenes y derechos:** qué gráfica revelar, qué hallazgo sustenta, interacciones accesibles, fuentes que permitan imágenes o enlaces alternativos, QA.

**DR-E Síntesis adversarial:** conciliar fuentes, disputas, lagunas, generar preguntas O1→O2→O3, diseñar modelo/estadística, filtrar factibilidad y priorizar arcos.

Cada afirmación externa se almacena como registro trazable: `claim_id`, `text`, `source_url`, `primary_or_secondary`, `evidence_date`, `accessed_at`, `supports`, `contradicts`, `confidence`, `used_in_question_ids`.

## 3. Datos y muestra
- `sample_raw.csv`: 10–20 registros verdaderos **no solo primeras filas**; cubrir distintos periodos/grupos, extremos, nulos y casos problemáticos cuando existan.
- `sample_features.csv`: transformaciones explícitas y comparables, **sin presentar el sample como representativo ni usarlo para estimar tasas poblacionales**.
- `metadata.json`: productor, fuente, licencia, URL de descarga/consulta, fecha de última verificación, inicio/final de datos, actualización, tamaño real bytes, filas, columnas, llaves, unidad, geografía, temporalidad, almacenamiento y cuotas, nulos y sesgos, hash, fecha de snapshot; los desconocidos son `PENDIENTE`.

## 4. Preguntas
- Las preguntas antiguas son insumos, no sección propia. **Un único banco** `QUESTIONS_MASTER.*`.
- 8–15 preguntas investigables por fuente cuando la riqueza lo justifique (sin forzar un número), priorizadas en 3–5 arcos narrativos.
- Para **cada pregunta**: O1, O2 con trigger O1, O3 con trigger O2; pregunta madre; hipótesis rivales; grano, denominador, baseline, variables/fuentes y estado.
- Para **cada pregunta**: al menos **un modelo propuesto** y un **ejercicio estadístico formal distinto** (método, razón, ubicación, requisito de datos, validación y riesgos).
- Un problema de tipo causal debe probar identificación; si no, limitarse a descripción y contradicciones.
- No entrenar modelos ni ejecutar pruebas por default durante el diseño del paquete.
- Toda pregunta ofrece figura principal, figura adversarial y potencial interacción verificable.

## 5. Prioridad de modelos
Selección conforme a tarea, escala, tamaño y target. Preferir GLM, beta-binomial, modelos mixtos, clustering binario, detección de anomalías, Fisher, bootstrap y permutaciones cuando correspondan. Para casos distintos pueden aportar LSTM/transformers, riesgos colectivos, Optuna y RL **solo con serie suficiente, outcome/reward, splits y evaluación**. Consultar `MODEL_SET.md`; jamás inventar utilidades de un modelo.

## 6. Gate de calidad del Paquete de Entrada
- Inventario y hash correctos, contexto externo con conflictos señalados.
- Muestra genuina con criterio de selección documentado.
- Una sola sección editorial integrada de preguntas; no «2B».
- 100% de preguntas con modelo, prueba estadística, razones, dónde, supuestos y estado; 100% con O1/O2/O3.
- Cero inferencias sobre salud/personas/causalidad sin evidencia.
- Visualizaciones con denominadores, derechos, fuente, incertidumbre y fallback.
- Lotes y límites de 45 minutos incluidos; no vender una clase como completada antes del ensayo.
- Estado `ENTRY_READY_FOR_REVIEW`, no `RESEARCH_APPROVED`.

## 7. Tres puertas de salida obligatorias
**Fase 0 → Fase 1:** el paquete es coherente y permite construir `research_guide.html`.

**Fase 1 → Fase 2:** usuario aprueba explícitamente la versión/commit de la guía científica. Entonces recién se permite el HTML audiovisual (guion/storyboard).

**Fase 2 → Fase 3:** usuario aprueba el guion/storyboard. Entonces recién se permite render de video.

Sin autorización, detenerse. No confundir historia de investigación con guion de video.

## 8. Formato de handoff
`START_HERE_NEW_CHAT.md` contendrá repositorio, ramas/PR, rutas, restricciones de escritura, contexto histórico resumido, conteos, gaps, modelo-set, preguntas priorizadas, comandos QA, definición de terminado, aprobaciones y prompt literal de siguiente turno. Una conversación nueva puede iniciar únicamente con este archivo.
