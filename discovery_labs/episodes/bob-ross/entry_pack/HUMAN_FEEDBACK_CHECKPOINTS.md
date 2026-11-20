# Bob Ross · Plan de Human Feedback científico (HF-00 → HF-04)

> **Estado:** protocolo listo para usarse; **ningún reporte de este documento representa un hallazgo ejecutado ni una aprobación**. Plantillas reutilizables en `discovery_labs/shared/templates/HUMAN_FEEDBACK_CHECKPOINT_TEMPLATE.md`, `HUMAN_FEEDBACK_REPORT_TEMPLATE.html` y `HUMAN_FEEDBACK_CHECKPOINT_SCHEMA.json`.
>
> **Objetivo:** llevar a la persona que revisa desde «¿qué tenemos?» hasta «¿qué resultado comprobamos y cómo lo contamos?», con informes que empiezan siempre por **RESUMEN EJECUTIVO** y tienen gráficas científicas excelentes, no decorativas.

## 1. Dónde aparecen en el flujo que ya existe

```text
DR-01 / DR-02 / DR-03 recibidos
       │
       ▼
QA de CSV, fuentes, derechos, claims, conciliación 14 BR ↔ 10 H
       │
       ├──────────► HF-00 · BRÚJULA Y PRIORIDAD ◄──────────┐
       │             decisión sobre 3–5 arcos, no final     │
       ▼
HTML F1 v0 con O1 solamente + ejecución reproducible de O1
       │
       ├──────────► HF-01 · DESCUBRIMIENTOS O1 ◄───────────┤
       │             primeras sorpresas o nulos honestos    │
       ▼
DR-05a · triangulación adversarial de O1 y DR-01/02/03
       │
       ├──────────► HF-02 · DECIDIR QUÉ O2 MERECEN SEGUIR ◄┤
       │             gate humano de prioridades             │
       ▼
O2 ejecutadas si respaldadas; O3 solo si O2 + rival real;
DR-04 visual/licencias (cuando haya insights elegidos)
       │
       ├──────────► HF-03 · ROBUSTEZ Y NARRATIVA CIENTÍFICA ◄┤
       │             excluir exageraciones y falsos efectos │
       ▼
DR-05b + actualización progresiva HTML F1 + reproducibilidad,
QA técnico, visual, derechos y enseñanza
       │
       └──────────► HF-04 · APROBACIÓN F1 (POR COMMIT) ◄─────┘
                     │
           Solo con RESEARCH_APPROVED:<commit>
                     ▼
       Fase 2 audiovisual (checkpoint HF-05 opcional)
                     │
           Solo con STORY_APPROVED:<commit>
                     ▼
       Fase 3 video
```

**No hay checkpoints obligatorios cada día ni uno por cada gráfico.** Se crean al pasar hitos con evidencia. Si un trabajo se bloquea por derechos o falta de datos, informar en el siguiente hito de orientación o decisión y conservar estado `BLOCKED`.

## 2. Atributos universales del informe Bob Ross

Cada `report.html` debe comenzar justo después de título/fecha con **Resumen ejecutivo** autónomo (100–180 palabras o menos sin resultados): hallazgo central o ausencia, avance respecto a versión anterior, explicación sorprendente que sí se sostiene, consejo concreto y una incertidumbre relevante. **Ninguna gráfica por encima del resumen.**

A continuación debe mostrar, en este orden:

1. **Qué cambió:** «Antes → Ahora» con IDs de preguntas y versiones de evidencia; primera HF-00 compara contra Entry Pack no contra checkpoint imaginario.
2. **El hallazgo inesperado:** como máximo una afirmación protagonista, con etiqueta `VERIFIED`, `REFUTED`, `INCONCLUSIVE` o `PENDING` justificada. Un nulo interesante puede ser protagonista; no llamar «wow» a un resultado por diseño.
3. **Gráficas**, preferentemente 2–4 si hay datos: una principal, una de robustez, una adversarial, opcional una de cambios/coverage. Mostrar menos si no hay datos verificados. En móvil prioridad a un gráfico legible por pantalla; detalles detrás de interacción accesible.
4. **CÓMO / POR QUÉ / PARA QUÉ** en lenguaje humano; números, denominador, baseline, incertidumbre, método, fuente, contraargumentos y siguiente experimento.
5. **Preguntas para JC: máximo tres** con opción o enfoque recomendado, coste, riesgos y efecto de posponer. Solo pedir decisiones que cambien el trabajo.
6. **Sugerencias** ordenadas por valor científico, esfuerzo y permisos; acción de continuar/parar/reenfocar; documento `feedback.md` con estado de respuesta.
7. **Evidencia:** código reproducible, CSV/JSON permitido, commits, SHA, fuentes, QA visual, licencias y registro de cambios.

**Carpeta principal:** `discovery_labs/episodes/bob-ross/human_feedback/HF-XX/vNN/` con `report.html`, `feedback.md`, `checkpoint.json`, `charts/` y `data/`, más `human_feedback/README.md` índice de revisiones. Versión y archivo inmutables para poder inspeccionar qué cambió.

## 3. Checkpoints concretos

### HF-00 · Brújula científica y auditoría

- **Ubicación:** **después** de auditar CSV, fuentes DR-01/02/03 y construir el mapeo BR-01..14 ↔ H1..10; **antes** de seleccionar y ejecutar en profundidad 3–5 O1.
- **Resumen debe responder:** qué tan confiable es lo que tenemos, qué contradicciones corregimos, qué 3–5 arcos prometen descubrir algo interesante, y qué bloqueos impedirían una conclusión.
- **Gráficas propuestas, solo cuando la auditoría esté ejecutada:**
  - Cobertura de evidencias por tema/fuente y estado de verificación (`VERIFIED/DISPUTED/PENDING/BLOCKED`) con denominadores.
  - Matriz de disponibilidad/prerrequisitos por 14 preguntas BR (CSV, paletas, imágenes/licencias, cronología) y riesgos.
  - Distribución inicial de las 67 etiquetas y tipos de datos, distinguiendo 381 episodios de Bob vs 22 de invitados **solo cuando se haya comprobado**.
- **Sorpresa buscada, NO hallazgo actual:** ¿diferencias reportadas de 3,221/3,224/3,324 etiquetas provienen de poblaciones, filtros o errores? Dejarla sin respuesta hasta calcular.
- **Avance sobre versión previa:** DR recibidos y banco diseñado → evidencia contrastada, población/llaves verificadas y top 3–5 priorizado.
- **Preguntas al usuario:** (1) ¿elegimos máxima novedad o máxima ejecutabilidad cuando compiten? (recomendar equilibrio con un arco bajo riesgo); (2) ¿qué 3–5 arcos quieren priorizarse? (proponer ranking); (3) ¿cuánto esfuerzo adicional se justifica para obtener imágenes autorizadas? (default: no bloquear O1 de CSV).
- **Exit:** tablas de reconciliación, prueba SHA/403×69, discrepancias cuantificadas o bloqueadas, lista de 3–5 O1 con criterios.

### HF-01 · Primeros insights reales y dudas inesperadas

- **Ubicación:** después de **1–2 O1 realmente ejecutadas** con scripts, muestras/denominadores, tests, cifras/IC y reproducción; no después de solo diseñarlas.
- **Gráficas candidatas:**
  - **H8**: adyacencias observadas de temas dentro de temporada frente a distribución nula de **10,000 permutaciones** que preserven conteo por temporada; p e intervalo de permutación, sin atribuir intención editorial.
  - Diferencia de resultados con los 22 invitados incluidos/excluidos y variación por temporada, siempre sobre universo verificado.
  - **H6 si existe ejecución:** estabilidad de clústeres vs métrica (Jaccard, Euclídea, ARI/Silhouette), nunca mostrar un k «verdadero» por estética.
- **Sorpresa:** por ejemplo, el patrón que se esperaba encontrar puede desaparecer tras estratificar; esto es **hipótesis de resultado posible, no hallazgo actual**.
- **Delta:** del plan a ejecución medible (preguntas respondidas, refutadas, inconclusas; bugs/filtros corregidos; cuantificar).
- **Preguntas al usuario:** ¿qué anomalía merece profundización? ¿prefieres perseguir un contraste inesperado aunque contradiga intuiciones? ¿qué ejemplo explicaría mejor esto a un alumno principiante?
- **Exit:** al menos un O1 con evidencia, figura principal y adversarial reproducibles; otras preguntas `PLAN_ONLY/BLOCKED` explícitas.

### HF-02 · Decisión de investigación de segundo orden

- **Ubicación:** una vez conciliados **resultados O1 + DR-01/02/03 + DR-05a**; inmediatamente **antes de activar O2**.
- **Gráficas candidatas:**
  - Mapa de evidencias: O1 → evento/claim externo → explicación rival → O2 posible; usar grafo o matriz con estado e incertidumbre.
  - Ranking de O2 por impacto científico, poder discriminante, coste y disponibilidad; barra comparativa solo si puntuación y pesos son explícitos.
  - Figura de sensibilidad que muestre cuánto cambió la conclusión O1 al cambiar filtros, pruebas, denominadores o baseline.
- **Sorpresa:** mitos falsados o conexiones históricas que **resisten** los controles, nunca correlación biográfica etiquetada causal.
- **Delta:** de métricas aisladas O1 a decisiones O2 con disparadores explícitos (`parent_id`, `trigger_evidence`).
- **Preguntas al usuario:** para cada ruta significativa ¿O2 ahora / aplazar / detener? ¿aceptar enriquecimiento externo legal y coste conocido? ¿qué narrativa sería didáctica **sin sobreinterpretar**?
- **Exit:** `O2_ACTIVATION_REVIEWED`, decisiones y estado humano registrado. Si no responde, no marcar `APPROVED` ni activar las O2 que requieren este gate.

### HF-03 · Robustez, visuales y qué descartamos

- **Ubicación:** después de las O2 seleccionadas, O3 si se justifica, y trabajo visual DR-04 pertinente; antes del cierre DR-05b.
- **Gráficas candidatas:**
  - Forest plot de tamaños de efecto/IC por subgrupo, transformación o variante de modelo.
  - Antes/después del control adversarial: efecto bruto frente al ajustado; mostrar resultados que pierden significancia.
  - Comparación de diversidad de motivos/paletas o estabilidad de modelos solo con fuentes autorizadas; detector de outliers con vista por SxxEyy.
- **Sorpresa:** el resultado que más cambió tras controles; si no sobrevivió, explicitarlo en el resumen.
- **Delta:** de O1/O2 preliminar a robustez, falsaciones y selección responsable de 3–5 conclusiones.
- **Preguntas al usuario:** ¿qué hallazgo enfatizar sin exagerar? ¿qué límite debe mostrarse a los alumnos? ¿qué visualización explica mejor un contraejemplo?
- **Exit:** figuras inspeccionables en móvil y teclado, fuentes/licencias, criterios de narrativa científica y matriz de hallazgos aceptados/refutados/inconclusos.

### HF-04 · Aprobación de guía científica

- **Ubicación:** después de DR-05b, `research_guide.html` progresivo, QA de datos/figuras, pruebas de reproducibilidad y lectura docente; **antes** de escribir storytelling audiovisual.
- **Gráficas candidatas:** selección editorial de 3–4 figuras finales con fuente/IC/contraargumento; comparativa «lo que creíamos vs lo que medimos» con denominadores y cautelas; evolución de cobertura/reproducibilidad entre checkpoints.
- **Sorpresa:** la conclusión científica con más respaldo y mayor poder pedagógico, acompañada del hallazgo refutado que evita una historia demasiado simple.
- **Delta:** del HF-03 a guía final validada (preguntas, resultados, correcciones, derechos, accesibilidad, rendimiento y enlaces).
- **Preguntas al usuario:** (1) ¿apruebas esta **versión/commit** del HTML como investigación científica? (2) ¿qué hallazgo merece ser la apertura de la clase? (3) ¿hay alguna interpretación que debamos matizar antes de guion?
- **Exit bloqueante:** guardar aprobación humana explícita como `RESEARCH_APPROVED:<commit_sha>`, o `CHANGES_REQUESTED` vinculada a versión. Un PR fusionado **no equivale a aprobación**.
- **Próximo paso si se aprueba:** Fase 2 storytelling; otra revisión humana HF-05 antes de video.

## 4. Aceptación por ciencia y visualización

- [ ] Resumen ejecutivo **primero**; decide rápido qué aprendimos, qué cambió y qué sigue.
- [ ] El reporte muestra un avance honesto sobre HF anterior o paquete de entrada, también cuando corrige una conclusión.
- [ ] Cada «wow» está marcado con **evidencia reproducible** o se declara todavía una hipótesis.
- [ ] Figuras 2–4 cuando hay datos (sin forzar tres): principal + robustez + rival; todas con n, denominador, fuente, unidad, incertidumbre, baseline y `chart_id`.
- [ ] Diseño responsive, SVG legible, contraste adecuado y alternativa teclado/tap/tabla; revisar 360px y 1280px.
- [ ] Material pictórico protegido **no** se incrusta sin derechos; usar gráficos originales de etiquetas/datos legales.
- [ ] Máximo tres preguntas importantes, sugerencia recomendada y consecuencia de no responder.
- [ ] `checkpoint.json` válido contra schema, `feedback.md` con estado real, sin aprobación inventada; versión `vNN` no se reescribe en silencio.
- [ ] CÓMO / POR QUÉ / PARA QUÉ, baselines, refutaciones, bloqueos y reproducibilidad.
- [ ] HF-02 y HF-04 no se dan por aprobados sin respuesta explícita o autorización previa documentada del alcance.

## 5. Relación con otros archivos

Este protocolo **complementa** [RESEARCH_PLAN.md](RESEARCH_PLAN.md) y el [HANDOFF_2026-11-19.md](HANDOFF_2026-11-19.md). No reemplaza `QUESTIONS_MASTER.md`/`questions_master.json` ni modifica el HTML V3 existente. La primera entrega real a crear será `human_feedback/HF-00/v01/report.html` **después** de ejecutar QA del dataset, no antes. La fecha de ese checkpoint será la de la ejecución y no la de este plan.
