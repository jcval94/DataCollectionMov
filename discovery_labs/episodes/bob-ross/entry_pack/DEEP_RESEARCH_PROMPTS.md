# Deep Research — cuatro investigaciones paralelas + síntesis

**Caso:** Bob Ross · `bob-ross-elementos` · `The Joy of Painting` · 31 temporadas etiquetadas · 403 episodios (381 anfitrión, 22 invitados).

Estas son instrucciones para una **IA con navegación y acceso a fuentes**. No sustituyen los resultados de una investigación efectivamente realizada. Los hechos externos se marcarán `VERIFIED`, `DISPUTED`, `CONTEXT_ONLY`, `PENDING` o `NOT_SUPPORTED`.

## DR-01 — Biografía, trayectoria y contexto histórico

> Eres historiador de medios y científico social. Investiga la **historia de Bob Ross**, su aprendizaje, los años en Alaska, la influencia de Bill Alexander, el nacimiento y funcionamiento de *The Joy of Painting*, las decisiones de producción de los años 1983–1994, el entorno de PBS, su negocio de materiales, sus colaboradores y los principales eventos personales documentados.
>
> Construye una línea de tiempo **con fecha, precisión, tipo de fecha (grabación/emisión/evento), fuente primaria o secundaria y nivel de confianza**, distinguiendo lo verificable de lo legendario.
>
> Investiga con particular cuidado el diagnóstico de linfoma y el final de la serie: **NO des por hecho que un cambio en motivos, color o complejidad fue causado por la enfermedad**. Verifica qué es realmente conocido sobre la fecha del diagnóstico, tratamientos, continuidad de grabación, cuánto duraba la producción por temporada y cuál fue el último episodio filmado versus emitido. Cuando no se conozca, marca PENDIENTE. No infieras estados emocionales ni síntomas del arte.
>
> Contrasta al menos dos fuentes periodísticas independientes y, cuando existan, entrevistas, archivos PBS, documentación de Smithsonian y fuentes de producción; no trates a una wiki o un documental promocional como confirmación suficiente.
>
> Incluye la información sobre las **siete pinturas preparadas para la temporada 32**, explica por qué podrían no estar entre los 403 episodios y qué sesgo de cobertura introduce. Investiga los derechos para mostrar pinturas.
>
> Entrega `timeline_events.csv`, `biography_sources.md`, `claims_registry.json`, `contextual_hypotheses.md` y 10 preguntas científicas de contexto que NO sean afirmaciones causales sin prueba.

**Pistas iniciales, no sustitutos de verificación:** [NPR/KPBS, 2016](https://www.kpbs.org/news/2016/08/28/the-real-bob-ross-meet-the-meticulous-artist), [Outside + Walt Hickey](https://www.outsideonline.com/podcast/bob-ross-strategies-survival/), [AP, siete pinturas de la temporada 32](https://apnews.com/article/bob-ross-painting-unfinished-season-nichola-hankins-cd50203eb6b3cf4f1893364cfae472be), [Smithsonian](https://amhistory.si.edu/docs/NMAH_report_2019.pdf).

## DR-02 — Arqueología del dataset, cronología y fuentes complementarias

> Eres Data Archaeologist y Senior Data Engineer. Audita el CSV `elements-by-episode.csv` (403 filas, 69 columnas, 67 etiquetas binarias) contra su commit original fijado por hash. Documenta qué constituye una observación y qué NO puede inferirse de esas etiquetas. Revisa nombres, duplicados semánticos, coetiquetado, episodios invitados y variables derivadas por OR. Busca cómo se produjo la codificación y sus limitaciones.
>
> Crea una tabla de episodios con temporada, episodio, fecha de emisión **verificada** y fecha de grabación si se encuentra; no conviertas SnnEnn automáticamente en un calendario. Anota diferencia entre fecha de grabación y emisión, riesgos de sindicación/reemisiones y datos faltantes. Si la fecha falta, conserva el orden de temporadas como secuencia ordinal.
>
> Investiga, separadamente, los datasets de **paleta/color**, metadatos de pinturas, enlaces a episodios y obra visual, por ejemplo `jwilber/Bob_Ross_Paintings` y los catálogos del mismo DataCollectionMov. Propón joins mediante `(season,episode)` con test 1:1, cobertura y casos no coincidentes. La licencia CC BY 4.0 de FiveThirtyEight NO se traslada a reproducciones visuales.
>
> Produce: diccionario exhaustivo, perfilado, matriz de completitud, posibles `snapshots` enriquecidos y contratos Silver/Gold; scripts reproducibles de unión y un informe de riesgos. **No descargues ni versiones imágenes sin permiso.** Evita mezclar datos de episodios emitidos con obras alternativas no equivalentes.

**Fuentes base:** [FiveThirtyEight](https://github.com/fivethirtyeight/data/tree/4c1ff5e3aef1816ae04af63218015066e186c147/bob-ross), [jwilber/Bob_Ross_Paintings](https://github.com/jwilber/Bob_Ross_Paintings), [investigación bibliográfica 2014](https://doi.org/10.1002/meet.2014.14505101084).

## DR-03 — Mitos, recepción, antecedentes y mecanismos

> Eres investigador de cultura popular, métodos históricos y diseño de hipótesis. Identifica afirmaciones **REALMENTE documentadas** sobre Bob Ross: árboles felices; espontaneidad; paisajes de Alaska; originalidad versus repetición; evolución de motivos, técnica y paleta; el negocio de materiales; relación entre show y obras; y otras observaciones con evidencia.
>
> Para cada creencia, captura **quién la dijo, cuándo, dónde, cita breve o paráfrasis precisa, URL, popularidad demostrable o no, contraafirmación y dataset capaz de contrastarla**. No fabriques mitos porque sean fáciles de comprobar. Si solo es provocadora, etiquétala `PROVOCACION_NO_MITO`.
>
> Busca análisis previos con resultados y métodos (FiveThirtyEight/Walt Hickey, trabajos de visualización de 2014, comunidades de análisis) y registra si son `DOCUMENTADO`, `REPRODUCIDO`, `PROPUESTO` o `NO_ENCONTRADO`. Distingue análisis de fuente primaria de copias y visualizaciones sin investigación.
>
> Investiga explicaciones rivales para cambios aparentes: demanda didáctica, producción del programa, recomendaciones de materiales, invitación de artistas, tendencias de época, disponibilidad de pinturas, etiquetado y sesgos de selección. Evita postular causalidad clínica/psicológica.
>
> Entrega `myths_claims.csv`, `antecedents.csv`, `rival_explanations.md`, `questions_to_test.json`.

**Fuentes iniciales:** [NPR/KPBS](https://www.kpbs.org/news/2016/08/28/the-real-bob-ross-meet-the-meticulous-artist), [FiveThirtyEight/Data](https://fivethirtyeight.datasettes.com/fivethirtyeight/bob-ross~2Felements-by-episode), [Wiley poster sobre visualización](https://doi.org/10.1002/meet.2014.14505101084).

## DR-04 — Investigación visual, imágenes, diseño y licencias

> Eres investigador en cultura visual, diseñador de visualizaciones y especialista en derechos. Diseña una colección de **visualizaciones que hagan visibles relaciones reales**, no que decoren cifras. Propón: línea temporal por temporada con incertidumbre; heatmap de motivos por temporada; contribución de huéspedes; coocurrencias frente a baseline; outliers por episodio/temporada; cambios de composición; cluster explorer con representantes reales; tarjetas de evidencias; vistas de sensibilidad (Jaccard vs Euclídea; K-means vs k-medoids cuando proceda).
>
> Para cada gráfico especifica pregunta, variable, unidad, denominador, cálculo exacto, baseline, incertidumbre o prueba adversarial, acción de usuario, texto alternativo, resolución y fuente. Diseña un *hover/focus card* por episodio: código, título, temporada, motivos y pertenencia al grupo; incluir la pintura real **solo si sus derechos permiten mostrarla**, y en ese caso describir archivo, licencia y autor. En caso contrario, mostrar una tarjeta de motivos derivada del CSV y un enlace al proveedor original (no incrustar ni descargar su imagen).
>
> Investiga licencias y términos de Three sources: FiveThirtyEight (etiquetas CC BY 4.0), Two Inch Brush (reproducciones) y jwilber (metadata/rutas). Comprueba restricciones de redistribución, hotlinking y capturas de pantalla; una URL pública no equivale a una licencia libre.
>
> Entrega `visuals_spec.md`, `preview_rights.csv`, `charts_evidence.json`, una maqueta técnica de explorador (sin inventar imágenes) y criterios QA de escritorio/móvil/teclado.

## DR-05 — Síntesis, triangulación y preguntas de orden superior (ejecutar DESPUÉS de DR-01 a DR-04)

**Nueva regla editorial V2:** Produce **un solo banco** `QUESTIONS_MASTER.md` y `questions_master.json`; las preguntas viejas A/B/C/D1/D2/E son subejercicios integrados, no sección aparte. Cada pregunta principal debe **proponer** (no entrenar) un modelo tomado de `MODEL_SET.md` y un ejercicio estadístico formal, declarando qué/por qué/dónde/condiciones y validación. Debe haber O1→O2→O3, con O2/O3 condicionales. La hipótesis de enfermedad ha de estar en el núcleo y su cronología es DISPUTADA: cotejar Outside, Washington Post, NPR y fuentes primarias antes de situar un evento en la línea temporal o sugerir causalidad.


> Actúa como editor científico adversarial. Lee las cuatro investigaciones, clasifica afirmaciones en `VERIFIED`/`DISPUTED`/`PENDING`, concilia fechas y poblaciones, elimina leyendas sin respaldo, detecta información que **no está** en el CSV y exige evidencia externa antes de convertirla en un hallazgo.
>
> Ejecuta la skill `question-forge`. Genera al menos doce preguntas raíz, con rutas O1→O2 y **al menos cuatro arcos que culminen en O3**, sin fingir resultados: cada O2/O3 indica el resultado previo que podría activarla. Selecciona de tres a cinco arcos prioritarios por potencial científico, visual, histórico y factibilidad.
>
> Construye un **mapa narrativo científico, no un guion audiovisual**: historia de Bob Ross en primer plano, eventos históricos como contexto, datos como prueba y tensiones derivadas de hallazgos observados. Entrega hipótesis rivales, DAG causal si resulta útil, matriz de triangulación entre fuentes, registro de creencias, diseños de análisis y planes de reproducción.
>
> No atribuyas un cambio estilístico a su enfermedad sin cronología verificable, controles, alternativas y estrategia de inferencia adecuada; si no es posible, presenta una investigación descriptiva de cambios y un apartado «lo que no podemos atribuir». No infieras estilos pictóricos a partir de etiquetas sin verificación visual independiente.
>
> Entrega `synthesis.md`, `question_graph.json`, `research_plan.md`, `source_claim_matrix.csv`, y criterios para construir `research_guide.html`. **DETENTE al llegar al límite de Fase 1: no escribir el guion de video ni producir video.**

## Regla transversal de las cinco investigaciones
Cada afirmación no trivial exige fuente, fecha o periodo, tipo de evidencia, nivel de confianza y uso previsto. Un reporte `VERIFIED` debe guardar URL estable, evidencia breve, fecha de consulta y posibilidad de refutación. Investigaciones inconclusas son resultados legítimos. Prioriza fuentes primarias y prensa de calidad; documenta desacuerdos sin forzar consenso.
