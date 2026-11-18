# MASTER PROMPT — Deep Research: la historia de Bob Ross antes que la tabla

## Misión
Actúa como un equipo de historiadores, periodistas de datos, estadísticos, curadores de arte, expertos en derechos, investigadores audiovisuales y diseñadores de preguntas científicas. Tu misión es investigar **la historia de Bob Ross y de la serie** de forma verificable para que el dataset pase de ser un conjunto de 403 episodios codificados a una investigación profunda y humana.

Esta es **Fase 0: Discovery Intake**. No construyas todavía el HTML de investigación, el guion audiovisual, la intro o el video.

## Entradas
- Fuente original: `../data/elements-by-episode.csv`, hash en `../data/manifest.json`.
- Muestra deliberada: `data_sample.csv` (NO representativa).
- Metadatos: `metadata.json`.
- Banco de investigación multinivel: `question_graph.json` y `QUESTION_GRAPH.md`.
- Evidencia inicial: `EVIDENCE_SEEDS.md`.
- Skill de preguntas: `skills/research-question-architect/SKILL.md`.
- Materiales previos: solo lectura; conserva hallazgos comprobados, distingue métodos.

## Ejecuta cinco investigaciones consecutivas

**01. Vida y eventos**, con `prompts/01_BIOGRAFIA_EVENTOS.md`. Especialmente cronología del diagnóstico, fechas de grabación vs emisión y si existe periodo pos-evento observable. Necesita contrastes y evidencia, no un supuesto psicológico.

**02. Contexto histórico y artístico**, con `prompts/02_HISTORIA_CONTEXTO.md`. Investiga la historia real de la serie de 1983 a 1994, cambios editoriales, pedagogía, influencias documentadas, artistas invitados, libros, versiones originales y proyectos incompletos.

**03. Literatura y experimentos previos**, con `prompts/03_CIENCIA_ANTECEDENTES.md`. Reúne artículos, notebooks, estudios, visualizaciones y su replicabilidad. Distingue 403×69 original de derivaciones y snapshots. Evita presentar descubrimientos ya conocidos como nuevos.

**04. Imágenes y derechos**, con `prompts/04_FUENTES_VISUALES_DERECHOS.md`. Examina uniones episodio→pintura, calidad de metadata, términos de uso para imágenes, thumbnails, tooltips y video. No copiar ni incrustar pinturas sin un permiso respaldado.

**05. Síntesis científica**, con `prompts/05_SINTESIS_HIPOTESIS.md`. Usa la evidencia de 01–04, activa la skill de preguntas y produce un grafo de primer/segundo/tercer orden. Selecciona preguntas prometedoras sin cerrar resultados antes del cálculo.

## Cómo investigar
- Prioriza fuentes originales, Smithsonian/PBS, archivos institucionales, entrevistas de primera mano, artículos académicos y el propio FiveThirtyEight. Registra por separado fuentes secundarias.
- Cada afirmación histórica importante debe tener URL verificable, fecha, cita contextual, grado de confianza y alternativa en caso de contradicción.
- Todo hecho ajeno al CSV se etiqueta EXTERNO_VERIFICADO, EXTERNO_EN_DISPUTA, HIPÓTESIS o DESCONOCIDO.
- Cruza cronologías antes de afirmar relación entre biografía y pintura. Los episodios fueron EMITIDOS en un orden; eso no prueba cuándo se pintaron.
- Por salud, evita diagnósticos retrospectivos a partir del color, los motivos, el gesto o las pinturas.
- No confundas la fuente de etiquetas CC BY 4.0 con derechos de imagen, nombre o video.

## Producto de Deep Research
1. `biography_timeline.csv` y `historical_context.csv`.
2. `evidence_ledger.csv` con afirmación, fuente, respaldo y discrepancias.
3. `prior_research.csv` y pruebas de reproducción.
4. `image_join_audit.csv`, `ASSET_RIGHTS.md`.
5. `question_graph_refined.json`, scorecards y 3 arcos priorizados.
6. Una narrativa **documental científica del episodio** con hechos y preguntas, todavía NO guion/escenas/minutaje.
7. Plan experimental y visual en `PLAN_DE_INVESTIGACION.md` actualizado.

## Entrega y puerta de calidad
Informa exactamente qué búsquedas efectuaste, qué información nueva encontraste, qué no se puede identificar y qué necesita más datos. Ningún hallazgo se promueve a guía HTML hasta contar con evidencia y cálculo. El usuario revisará este paquete antes de autorizar avances importantes.

**No hagas un resumen biográfico superficial: busca mecanismos, momentos de ruptura, materiales inéditos, excepciones y preguntas que todavía no se hayan respondido.**
