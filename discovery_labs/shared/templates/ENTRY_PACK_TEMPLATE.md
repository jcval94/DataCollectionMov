# Entry Pack — plantilla oficial de cualquier episodio de AI Discovery Labs

> Copiar/adaptar este contrato a cada nuevo dataset. La skill compartida `discovery_labs/shared/skills/question-forge/SKILL.md` lo consume. **No** construir guion ni video antes de aprobar el primer HTML.

## 0. Identidad del caso
- `episode_id`, slug, título provisional (sin revelar resultado), macrocategoría y audiencia.
- El problema humano: ¿qué historia, tensión, contradicción o decisión real vuelve interesantes los datos?
- Definición clara de unidad de observación, cobertura y periodo.
- Personas/organizaciones y derechos de imagen: no inferir hechos personales sensibles a partir de datos indirectos.

## 0 bis. Misión y triada obligatoria

**Objetivo de cada dataset:** descubrir insights increíbles por su **originalidad, evidencia e implicaciones**, no por su espectacularidad retórica. Registrar tanto sorpresas respaldadas como refutaciones, hallazgos nulos, sesgos y fronteras del dato.

Toda investigación, toda síntesis de resultado y el HTML deben responder por separado:

- **CÓMO:** datos, grano, pasos, modelo, ejercicio estadístico, baseline, incertidumbre y reproducción.
- **POR QUÉ:** relevancia de la pregunta, plausibilidad, hipótesis rivales y justificación del método; no inventar mecanismos.
- **PARA QUÉ:** implicación científica, práctica o educativa y siguiente acción/experimento; si no hay utilidad demostrable, decirlo.

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
    QUESTIONS_MASTER.md            # ÚNICA sección editorial de investigaciones
    questions_master.json          # Versión estructurada que alimenta el HTML
    VISUAL_DESIGN.md               # Argumentos visuales, QA y derechos
    PROMPT_FASE1.md                # Prompt propio para preparar guía científica
  research_guide.html              # ÚNICA guía de Fase 1, tras investigar
```

## 2. Cinco frentes de Deep Research, ejecutados en etapas

**No lanzar cinco investigaciones exhaustivas en paralelo.** Los cinco frentes son herramientas, no una cuota; ejecutar únicamente lo que aporte evidencia a la siguiente decisión. Toda fuente lleva `claim_id`, URL, fecha, estado y pregunta relacionada.

| Frente | Momento recomendado | Producto / decisión |
|---|---|---|
| **DR-A Historia y dominio** | **Temprano**, antes de interpretar O1 | Cronología de hechos relevantes, fuentes, incertidumbre y eventos externos |
| **DR-B Datos y accesos** | **Temprano**, antes de medir O1 | Procedencia, cobertura, licencias, grano, calidad, joins y límites |
| **DR-C Mitos y antecedentes** | **Temprano y focalizado**, antes de convertir intuiciones en hallazgos | Revisión de afirmaciones verificables, estudios previos, mecanismos y contraejemplos |
| **DR-D Visualización especializada y derechos** | **Profundizar después de O1 y selección de insights** | Figuras que prueban/contradicen el resultado, auditoría de imágenes y accesibilidad; **triage de licencias al inicio** |
| **DR-E Síntesis adversarial** | **Punto de control tras A/B/C + respuesta medida de O1**, y cierre tras D + O2/O3 | Activación justificada de O2, contradicciones, priorización y síntesis final |

**Secuencia:** contexto temprano DR-A/B/C → HTML v0 con O1 y sin adelantar O2/O3 → ejecutar y responder O1 → DR-E provisional → activar O2 justificadas → ejecutar O2 → abrir O3 si procede → DR-D específico y DR-E final → QA + aprobación humana. Reordenar DR-D si una visualización o licencia es requisito temprano de factibilidad. La existencia de un prompt **no significa que su investigación esté ejecutada**.

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
Selección conforme a tarea, escala, tamaño y target. Preferir GLM, beta-binomial, modelos mixtos, clustering binario, detección de anomalías, Fisher, bootstrap y permutaciones cuando correspondan. Para casos distintos pueden aportar LSTM/transformers, riesgos colectivos, Optuna y RL **solo con serie suficiente, outcome/reward, splits y evaluación**. Consultar `discovery_labs/shared/model_catalog/MODEL_SET.md`; jamás inventar utilidades de un modelo.

## 5 bis. Contrato del HTML inicial y sus actualizaciones

El archivo `research_guide.html` debe ser **un documento científico vivo, bien estructurado y versionado**:

1. **Párrafo de contexto general al principio** del contenido principal: historia o fenómeno, dataset, periodo, pregunta que importa, sin resultados ficticios.
2. Misión de descubrimiento y triada **CÓMO / POR QUÉ / PARA QUÉ**.
3. Fuente, unidad, cobertura, sesgos, licencias y preguntas no medibles.
4. **Único bloque visible de O1** y sus métodos, hipótesis, denominadores y estados; O2/O3 planeadas solo en los contratos internos hasta verificar resultados.
5. Evidencia y resultados con estados; hipótesis rivales y límites; utilidad real o pregunta abierta.
6. Reproducibilidad, fuentes, bitácora de cambios por versión/commit y gate de aprobación.

**Evolución comprobable:** registrar `version`, `question_id`, `parent_id`, `trigger`, `source_claim_ids`, `result_artifact`, `status` y fecha al publicar cada nueva pregunta. **O2** aparece únicamente tras O1 respondida y Deep Research temprano pertinente + síntesis provisional. **O3** aparece únicamente tras ejecutar O2 y evaluar hipótesis rivales. Un resultado nulo también puede abrir una nueva O2. Mantener intactos los IDs existentes y nunca sustituir una versión sin trazabilidad. La guía HTML V0 no equivale a una guía científica terminada ni autoriza video.

## 6. Gate de calidad del Paquete de Entrada
- Inventario y hash correctos, contexto externo con conflictos señalados.
- Muestra genuina con criterio de selección documentado.
- Una sola sección editorial integrada de preguntas; no «2B».
- 100% de preguntas canónicas con un modelo y ejercicio estadístico planificados, CÓMO/POR QUÉ/PARA QUÉ, razones, dónde, supuestos y estado; 100% con O1 y diseños O2/O3 **condicionales internos**. El HTML inicial solo publica O1.
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
`START_HERE_NEW_CHAT.md` contendrá repositorio, ramas/PR, rutas, restricciones de escritura, contexto histórico resumido, conteos, gaps, ruta al catálogo compartido, preguntas priorizadas, comandos QA, definición de terminado, aprobaciones y prompt literal de siguiente turno. Una conversación nueva puede iniciar únicamente con este archivo.

## Infraestructura única (NO copiar dentro de cada episodio)

- `discovery_labs/shared/skills/question-forge/SKILL.md`: metodología y rúbrica común.
- `discovery_labs/shared/model_catalog/MODEL_SET.md`: catálogo único de 24 familias.
- `discovery_labs/shared/templates/ENTRY_PACK_TEMPLATE.md`: esta plantilla.
- `discovery_labs/shared/templates/DEEP_RESEARCH_TEMPLATE.md`: prompts generalizables para investigación contextual.
- `discovery_labs/shared/validators/validate_entry_pack.py`: validar un paquete con `--entry-pack ...`.

Cada episodio puede tener `MODEL_FIT.md` (selección **específica** de modelos del catálogo y razones, sin copiar la lista de 24), además de `QUESTIONS_MASTER.*`, `START_HERE_NEW_CHAT.md`, `metadata.json`, muestras y su `research_guide.html`. La validación lee un solo catálogo compartido; no se admiten copias independientes de la skill o del set de modelos.

Si el caso ya usa rutas antiguas, crear un **shim/archivo de transición** que apunte a shared y ejecutar tests antes de eliminar cualquier ruta.
