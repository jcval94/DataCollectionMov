# Plan de investigación V2 — Bob Ross

## Norte

**La historia de Bob Ross debe ser la columna vertebral de la investigación científica**, no únicamente una excusa estética para colorear gráficos. Cada pasaje biográfico requiere fuente, fecha y vínculo explícito —o imposibilidad de vínculo— con la evidencia del dataset. El protagonista sigue siendo el dato y sus límites.

## Entregables y puertas

| Puerta | Entregable | Aprobación |
|---|---|---|
| 0 | Este paquete de entrada: datos de muestra, metadata, prompts DR, mapa de preguntas profundas, fuentes, brief visual y plan | Revisión editorial / datos |
| 1 | `research_guide.html`: historia, hechos, análisis reproducidos, código, gráficos, pruebas y límites | **Aprobación EXPLÍCITA del usuario sobre versión/commit** |
| 2 | `video_storytelling.html`: guion audiovisual, introducción, escenas, voz, ritmo, storyboard y transición | **Bloqueada hasta aprobación fase 1**; después aprobación EXPLÍCITA adicional |
| 3 | Video renderizado MP4, subtítulos y audio | **Bloqueada hasta aprobación fase 2** |

No producir intro de video, spritesheet, storyboard audiovisual, música, Remotion ni MP4 durante fases 0/1.

## Pregunta editorial: ¿qué historia contar?

**Capa humana:** el artista, su método, el programa televisivo y sus 31 temporadas; aquello que sabemos por fuentes de calidad. No adelantar hipótesis de enfermedad como hecho.

**Capa de datos:** cada episodio tiene etiquetas de presencia, no trazos, belleza ni fecha de producción. Distinguir años de emisión de años de pintado. 403 episodios etiquetados, 22 invitados, 381 del anfitrión.

**Capa de investigación:** de patrones generales a cambios por periodo y casos atípicos; tomar decisiones basadas en resultados. Una pregunta puede producir varias ramas secundarias pero cada clase vota una ruta que quepa en 45 minutos.

**Capa de aprendizaje:** el alumno hace una apuesta, entiende denominadores, cuestiona el trabajo de IA, encuentra un contraejemplo y firma una interpretación.

## Secuencia de ejecución (no saltar pasos)

### Bloque A · DR 1/2/3/4 con fuentes
1. Investigar la cronología (DR-1).
2. Revisar análisis previos y fuentes adicionales (DR-2).
3. Generar/revisar preguntas de 1.º/2.º/3.er orden (DR-3 y skill).
4. Construir inventario de activos y reglas de visualización (DR-4).
5. Realizar síntesis crítica DR-5.
**DoD:** registro de claims, fechas, URLs y fuentes por tipo, conflictos declarados.

### Bloque B · Data readiness
1. Validar SHA de Bronze y esquema binario; conservar original.
2. Construir Silver por episodio y temporada, dejando `GUEST` explícito.
3. Enriquecer con fechas de emisión y, si existen, grabación; validar 403/403 relaciones o reportar faltantes. Nunca asumir que año de emisión es fecha de pintura.
4. Enriquecer con paletas para investigar color; verificar unidades, cobertura, licencias y join uno-a-uno.
5. Preparar dataset de imágenes/vínculos con derechos por registro; imágenes remotas sólo bajo términos permitidos.
**DoD:** QA con pérdidas, duplicados, divergencias y tasas por subgrupo.

### Bloque C · Investigación exploratoria + preguntas adaptativas
1. Evaluar 12 preguntas; elegir 3–4 por relevancia/viabilidad, no por facilidad computacional.
2. Hacer EDA exploratorio pero preservar la distinción entre descubrimiento y confirmación.
3. Ejecutar orden 1; documentar el patrón (o ausencia), sus denominadores y visual.
4. Solo entonces activar ramas de orden 2 y pruebas adversariales de orden 3.
5. Contrastar que cambios de periodo no son eventos causales sin identificación, fechas y alternativa.
6. Revisar outliers a nivel episodio, temporada y bloques temporales; corregir por exposición y tamaño.
**DoD:** pruebas reproducibles, tablas y figuras inspeccionadas, ningún resultado imaginado.

### Bloque D · Fase 1, investigación HTML
1. Abrir con la historia verificable, mostrar cronología y límites del dataset; usar referencias numeradas.
2. Narrar la investigación según hallazgos, sin forzar giro dramático.
3. Presentar visualizaciones interactivas: periodos, anomalías, motivos, transiciones de clusters y fichas de episodios.
4. Vincular cada claim a su script, snapshot, output, definición, denominador, fecha y fuente.
5. Alternar modo lector y modo técnico; captions/alt/teclado/tap.
6. Registrar QA visual escritorio/móvil y revisión científica independiente.
7. Entregar `research_guide.html` con estado `PENDIENTE_DE_APROBACIÓN`.
**STOP:** solicitar aprobación humana y NO comenzar storytelling audiovisual.

## Quality gate de una pregunta

| Criterio | Estatus esperado |
|---|---|
| Existen datos y derechos para la ruta | Confirmado |
| Orden 1 ejecutado y revisado | Confirmado |
| Ramificación orden 2 motivada por resultado | Confirmado |
| Orden 3 valida o contradice una explicación | Confirmado |
| Conclusión no es solo un conteo | Confirmado |
| Gráficos con magnitud, unidad, filtros y contexto | Confirmado |
| No implica causalidad sin identificación | Confirmado |
| Alternativa si falta el enriquecimiento externo | Documentada |

## Rendición de cuentas en cada lote

El investigador reporta: fuentes verificadas, claims confirmados/conflictivos, tablas reproducidas, preguntas o ramas ejecutadas, gráficos inspeccionados, evidencia faltante, cambios del repositorio y estado de la puerta. Un plan no cuenta como descubrimiento.

## Regla de aislamiento
Mantener cambios dentro de `discovery_labs/episodes/bob-ross/`; no tocar pipelines de movilidad ni el portal. La skill es portable, pero copiarla fuera de la carpeta queda para un cambio autorizado separado.
