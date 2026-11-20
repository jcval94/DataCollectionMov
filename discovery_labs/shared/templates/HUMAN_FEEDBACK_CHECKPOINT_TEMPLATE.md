# AI Discovery Labs — contrato reusable de Human Feedback v1

> **Para todos los datasets/episodios.** Este archivo prescribe cómo crear, evaluar y registrar checkpoints humanos durante una investigación; no contiene hallazgos de ningún episodio.
>
> **Objetivo:** que el investigador pueda decidir en menos de 3 minutos si una línea de investigación merece continuar, cambiar, bloquearse o aprobarse. No convertir la revisión en un dashboard de vanidad ni en un cuestionario largo.

## 1. Política central: primero resumen, luego gráficas

Cada checkpoint publica un **informe principal `report.html`**, autónomo y responsive (móvil/desktop), y un `feedback.md` con decisiones/versiones. El primer contenido visible debajo del título y fecha es **«Resumen ejecutivo»** — antes de estadísticas, tablas, metodología, navegación extensa o gráficas.

**Resumen ejecutivo obligatorio**, entre 100 y 180 palabras (o menos si no hay evidencia), que responde por sí mismo a:
1. **Qué aprendimos** desde el último checkpoint (resultado observado, refutación o bloqueo, nunca promesa).
2. **Qué cambió** respecto de la versión inmediatamente anterior: descubrimiento, corrección, dato nuevo, decisión o incertidumbre resuelta; comparar mismo universo y definiciones.
3. **Qué debería sorprenderme** y con qué grado de confianza; si no existe sorpresa respaldada, escribir literalmente «Aún no hay un insight sorprendente confirmado».
4. **Qué recomiendo hacer ahora** y **qué necesito que decida la persona** (máximo tres decisiones claras).
5. **Qué limita el resultado** en una frase concreta.

La primera pantalla debe contener el resumen, un estado visible de la investigación y una recomendación principal. **No** abrir con portada gigante, métricas desconectadas, visualización decorativa o una lista de 20 KPIs.

## 2. Checkpoints de ciclo científico

| ID | Momento exacto | Propósito | Salida/decisión | Gate humano |
|---|---|---|---|---|
| **HF-00: Brújula** | Tras auditar datos/DR tempranos, antes de seleccionar arcos O1 | Revisar confianza del dataset, top preguntas, límites y prioridades | Elegir 3–5 arcos investigables; registrar bloqueos | **Orientación**; cambios de prioridades se aceptan sin fingir evidencia |
| **HF-01: Primeros hallazgos** | Tras ejecutar al menos 1–2 O1 y reproducir sus resultados | Enseñar resultados, excepciones, negativos y efecto de filtros/modelos | Continuar, cambiar de método o detener un arco | **Feedback investigativo**; no publicar O2 por este reporte |
| **HF-02: Decisión O2** | Tras responder O1 seleccionadas y síntesis adversarial DR-05a | Confrontar O1, DR-01/02/03 y rivales | Aprobar/rechazar/priorizar **cada O2** propuesta | **Decisión explícita sobre profundización**; O2 requiere evidencia + revisión del gate, salvo autorización ya documentada |
| **HF-03: Robustez e interpretación** | Tras O2 ejecutadas, O3 si disparó, y DR-04 visual relevante | Probar sensibilidad, rivales, incertidumbre, visuales y alcance de afirmaciones | Elegir qué insights sobreviven y cuáles son inconclusos; cambios finales | **Feedback científico**; no aprobar Fase 1 por defecto |
| **HF-04: Aprobación de Fase 1** | Tras DR-05b, guía HTML actualizada, QA científico/visual y reproducibilidad | Mostrar investigación final vs versión previa, límites y demostraciones | Aprobar `RESEARCH_APPROVED:<commit_sha>` o pedir cambios | **Gate bloqueante** para pasar a storytelling audiovisual |
| **HF-05: Storytelling** | **Opcional fuera de la investigación científica**, solo cuando Fase 2 audiovisual existe | Revisar storyboard/guion y fidelidad a las evidencias | Aprobar `STORY_APPROVED:<commit_sha>` o pedir cambios | **Gate bloqueante** para producir video |

**Cadencia basada en evidencia, no calendario.** HF-00..04 se generan una vez por hito y pueden tener revisiones v2/v3 si cambian los hallazgos. Un mismo HF-01 puede agrupar varios O1: no interrumpir por cada métrica. Si no se ejecutan O2 o O3, HF-03 debe explicitar que están bloqueadas/descartadas, sin forzar investigación ficticia. HF-05 no sustituye el aprobado de Fase 1.

**Política de continuidad:** sin respuesta humana, se pueden ejecutar verificaciones y experimentos *reversibles* con el plan aprobado, pero no convertir supuestos en hechos, no promover O2 sin gate HF-02 cuando éste está requerido, no marcar estados como `APPROVED`, ni cruzar Fase 1→2 o Fase 2→3.

## 3. Carpeta y archivos obligatorios

Ubicación estándar por episodio:

```text
discovery_labs/episodes/<slug>/human_feedback/
  README.md                          # Índice de hitos, versiones, estados y última decisión
  HF-00/
    v01/
      report.html                    # Documento principal, primero Resumen ejecutivo
      feedback.md                    # Preguntas humanas, recomendación, respuesta y decisiones
      checkpoint.json                # Estado, evidencia, comparativo, visuales, QA y vínculos
      charts/                        # SVG/PNG offline, solo gráficos calculados
      data/                          # Agregados mínimos reproducibles y metadatos; sin material protegido
  HF-01/v01/...
  HF-02/v01/...
  HF-03/v01/...
  HF-04/v01/...
```

- **Inmutabilidad editorial:** si cambian datos o interpretación, crear `v02`, no sobrescribir `v01` sin rastro; actualizar `human_feedback/README.md` con enlace y diferencias.
- `report.html` se debe poder abrir sin red cuando los datos lo permiten. No guardar imágenes protegidas, video o otros activos sin licencia/autorización.
- `feedback.md`: propuesta, preguntas y estado de respuesta; registrar de forma atribuible **solo decisiones efectivamente comunicadas** por el usuario, con fecha/referencia; jamás inferir «aprobado».
- `checkpoint.json`: contrato mínimo en `HUMAN_FEEDBACK_CHECKPOINT_SCHEMA.json`; validar JSON y referencias antes de publicar.
- Un resultado nuevo requiere `evidence_ref` a script/dato/log/figura; un hallazgo sin prueba se marca `HYPOTHESIS` o `BLOCKED`.
- Guardar `source_commit`, `dataset_hash` cuando exista, `previous_checkpoint`, `question_ids`, fechas de evidencia y derechos de figuras.

## 4. Orden editorial exacto de report.html

1. **Título breve + ID/versión/fecha/estado** y, *de inmediato*, **RESUMEN EJECUTIVO**. Una primera pantalla comprensible en móvil.
2. **Lo que cambió desde la versión anterior:** tabla «Antes → Ahora → Evidencia → Impacto» con cambios científicos reales, incluso correcciones, nulos o rechazos. Para HF-00 utilizar línea base «Paquete de Entrada», no comparar contra una versión inventada.
3. **Hallazgo más sorprendente / hipótesis refutada / ausencia inesperada:** título entendible, tamaño de efecto, baseline, incertidumbre, rival más fuerte. Solo etiquetar como confirmado si hay ejecución reproducible.
4. **2–4 gráficas importantes cuando la evidencia lo permita**, comenzando por la figura que mejor explica el descubrimiento. Una gráfica principal, una comparación robusta y una adversarial; pueden sumarse una de progreso/coverage. HF-00 usa únicamente cobertura/calidad/plan, NO efectos científicos ficticios. Si solo hay 1 gráfica honesta, mostrar 1 y explicar el faltante.
5. **Qué significa CÓMO / POR QUÉ / PARA QUÉ**, con lenguaje claro; distinguir por qué *se eligió el método* de causalidad sobre el fenómeno.
6. **Preguntas para ti (máximo 3)**: cada una concreta, con opción A/B, recomendación por defecto, consecuencias, coste y qué pasará si no se responde; permitir pregunta abierta cuando de verdad importe.
7. **Recomendación y próximo tramo**: qué se investigará a continuación, qué no se investigará, bloqueos/recursos, definición verificable de éxito.
8. **Evidencia y reproducibilidad**: fecha/versiones, fuentes, código, hashes, filtros, métodos, n, denominadores, incertidumbre, contraargumentos, derechos y changelog completo.

Ninguna gráfica puede preceder al resumen ejecutivo. Metodología larga y referencias van al final o en acordeones accesibles.

## 5. Contrato visual: gráficas que revelan, no decoran

Cada gráfica debe responder una **pregunta científica explícita**. Mínimos:

- **Título en forma de conclusión sustentada o pregunta**, y descripción textual de lo observable. No nombrarla solo «Gráfico 1».
- `chart_id` estable, `question_id`, `evidence_ref`, `data_source`, `dataset_hash`, `code_ref`, `population`, `n`, `denominator`, unidad, periodo, transformación y filtros.
- Baseline o comparación explícita; cuando proceda, **intervalos de confianza**, bandas bootstrap, distribución nula, errores, tamaño de efecto y sensibilidad. Reportar incertidumbre o aclarar que no está disponible.
- Una **figura adversarial** sobre un rival o análisis de sensibilidad; visualizaciones comparativas con misma escala, intervalos y definición de muestra. No dual-axis sin motivo; no truncar ejes engañosamente; no interpretar p como tamaño de efecto.
- **Pertenencia al episodio y trazabilidad**: cuando sean puntos episodios, incluir SxxEyy; inspector accesible hover/focus/tap con título, categoría, muestra y fuente. Pantallas táctiles deben tener alternativa al hover.
- Responsive 360px+ y escritorio 1280px; leyendas legibles, contraste AA, soporte teclado, texto alternativo y resumen tabular cuando sea relevante; SVG/PNG accesibles y sin dependencia obligatoria de CDN.
- No usar pinturas, capturas o fotografías sin derechos verificados. En su lugar diagramas derivados de etiquetas/datos legales.
- No gráficas hechas con datos mock como si fueran evidencia. Plantillas pueden mostrar **«Sin resultados ejecutados»** y especificación del gráfico futuro, claramente separados.

**Verificación visual mínima antes de publicar:** revisar vista móvil y escritorio, todos los charts legibles sin hover, fuentes y números contra la tabla de resultados, ejes/unidades y alt text; comprobar que todo insight citado aparece en un objeto de evidencia, y que la figura adversarial **no se ocultó** por contradecir la historia.

## 6. Modelo de decisión por checkpoint

- Cada reporte declara `proposed_action`, `default_action`, `human_gate` y `decision_status` con valores `PENDING`, `APPROVED`, `CHANGES_REQUESTED`, `DEFERRED` o `REJECTED`. `PENDING` es el valor de salida si aún no respondió el usuario.
- Las preguntas deben distinguir **opinión/editorial** (p. ej., qué fenómeno contar) de **verificación factual** (p. ej., tamaño de muestra). El voto humano no cambia un p-value ni valida una fuente.
- Para cambios relevantes: `question_id`, alternativa A/B, recomendación justificada, `human_response` (solo si existe), `decision_date`, `changes_since_prior` y `next_action`.
- Si surge un insight contrario a hipótesis inicial, debe aparecer en el resumen y en el changelog, no esconderse como «pendiente».
- Una negativa o falta de respuesta de HF-02 no invalida O1: solo impide promover la investigación de segundo orden en esa ruta.

## 7. Definition of Done y publicación

**FAIL** si: falta resumen inicial; falta comparación con versión previa; se inventa una sorpresa; hay gráficas sin evidencia o muestra/denominador; falla la lectura móvil/teclado; no hay preguntas concretas; el estado de aprobación se asume; no existen enlaces a código/fuentes; los datos usados no corresponden a la versión declarada.

**PASS** si:
- [ ] El resumen abre el informe y es autónomo (respuesta, delta, sorpresa honesta, recomendación, bloqueo).
- [ ] El delta cuantifica/mejora lo que cambió (o declara «sin cambio medible»).
- [ ] Los gráficos relevantes se reproducen desde datos permitidos, tienen evidencia y contrapeso adversarial.
- [ ] Los hallazgos muestran efecto, incertidumbre, n, denominador y explicaciones rivales.
- [ ] Se contestan CÓMO / POR QUÉ / PARA QUÉ.
- [ ] Hay máximo tres preguntas para el usuario con recomendación, consecuencias y opción de posponer.
- [ ] Se registran gate, versión, precedente, evidencias, decisiones y rutas de outputs.
- [ ] La revisión de legibilidad móvil y escritorio está documentada.
- [ ] El reporte está separado de los resultados del HTML Fase 1; feedback no sustituye `RESEARCH_APPROVED:<commit>`.

**Plantilla visual base:** [HUMAN_FEEDBACK_REPORT_TEMPLATE.html](HUMAN_FEEDBACK_REPORT_TEMPLATE.html). No rellenar con datos sintéticos fingiendo análisis real.
