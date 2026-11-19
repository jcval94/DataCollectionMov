# Plantilla universal de Deep Research — todos los AI Discovery Labs

Esta plantilla se copia para un dataset nuevo y se rellena ANTES de crear su guía científica. Diseñada para ser portátil; no depende de Bob Ross.

## Variables de entrada

- `DATASET_ID`: [identificador]
- `PROTAGONISTA / FENÓMENO`: [persona, comunidad, institución, proceso o sistema]
- `PREGUNTA HUMANA INICIAL`: [tensión que interesa a un no especialista]
- `UNIDAD DE OBSERVACIÓN`: [registro, entidad, episodio, transacción...]
- `COBERTURA / FECHAS`: [de la fuente, no inferidas]
- `MUESTRA REAL`: [10–20 registros con procedencia]
- `LICENCIA / RESTRICCIONES`: [datos, imágenes, video por separado]
- `HIPÓTESIS PREVIAS`: [afirmaciones no demostradas]
- `RESULTADOS YA REPRODUCIDOS`: [con scripts/hashes]
- `EVENTOS EXTERNOS CANDIDATOS`: [no asumir su influencia]

## Prompt maestro genérico

> Actúa como un equipo de historiadores, especialistas de dominio, documentalistas, estadísticos, ingenieros de datos, investigadores causales y periodistas científicos. Investiga profundamente la **historia detrás de [PROTAGONISTA / FENÓMENO]**, con el objetivo de diseñar preguntas científicas memorables y falsables a partir de [DATASET_ID].
>
> Divide el trabajo en cuatro informes especializados y una síntesis crítica:
>
> 1. **Historia y contexto:** cronología de creación, hitos, decisiones, cambios tecnológicos, controversias y eventos externos. No confundas fechas de publicación, registro y evento; aporta fuentes originales, conflictos y precisión temporal.
> 2. **Estado del arte y universo de datos:** antecedentes reales, preguntas ya resueltas, datasets complementarios, cobertura, uniones, unidad, calidad, privacidad, derechos y lagunas. No llamar novedoso a lo ya publicado.
> 3. **Hipótesis y generación profunda:** usa la skill `research-question-architect` con ejes de cambios de régimen, outliers multiescala, paradojas de composición, variación/continuidad, teorías rivales, eventos externos y lo ausente. Por cada caso diseña 1.º orden medible, al menos dos ramas de 2.º orden disparadas por resultados observados y un 3.er orden adversarial/explicación rival. Las creencias populares necesitan evidencia de que son creencias extendidas, no un yes/no fácil.
> 4. **Visualización y derechos:** define gráficos que revelen conceptos, zoom desde agregados a registros concretos, ejemplos con hover/focus/tap y comparación de casos. Comprueba permisos distintos de datos, imágenes y videos; ofrecer alternativa sin recurso protegido.
> 5. **Síntesis red-team:** concilia afirmaciones y fuentes, identifica contradicciones, riesgos estadísticos y de derechos, produce ranking de preguntas y decide qué puede comprobarse. Diferencia `CALCULADO`, `DOCUMENTADO`, `HIPOTESIS`, `CONFLICTO`, `BLOQUEADO`.
>
> Entrega `timeline`, `claims_registry`, `evidence_map`, `external_join_plan`, `question_graph`, `visual_brief`, `risk_register`, `execution_plan` y criterios para aprobar la guía científica HTML. Cada afirmación contextual con URL, fecha, tipo de fuente, cita breve y confianza. Cada pregunta con variables, método, denominador, comparación alternativa y límites.
>
> No inventes ni fuerces cambios causales por coincidencia en fecha. No generes todavía guion audiovisual ni video. No comiences Fase 2 sin aprobación explícita del HTML científico.

## Criterios de calidad de salida

- Historia **real y verificable**, no una biografía inventada para adaptar al dataset.
- Al menos ocho ideas candidatas por fuente, con cuatro familias generalizables fuera de las perspectivas básicas.
- Una shortlist de 2–4 historias científicas capaces de interesar y enseñar, no 12 consultas triviales.
- Preguntas multinivel, con triggers concretos y desenlaces negativos contemplados.
- Pipeline y visualizaciones calculables; fuentes y licencias registradas.
- Prioridad a evidencias humanas, contenido y metodología por encima de adornos audiovisuales.
- Documento científico primero, dos aprobaciones explícitas, video al final.

## Adaptación al caso de Bob Ross

Usar los prompts enfocados en `DEEP_RESEARCH_PROMPTS.md`; este archivo es la plantilla para replicar el método en los demás datasets. Conservar la regla estricta de trabajo dentro de la carpeta del episodio.
