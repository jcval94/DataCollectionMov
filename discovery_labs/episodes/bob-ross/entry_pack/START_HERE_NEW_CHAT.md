> **Continuación científica:** [handoff O1/O2 del 19-11-2026](HANDOFF_2026-11-19_SCIENTIFIC_O1.md). Revisar antes de utilizar instrucciones históricas.

# START HERE — AI Discovery Labs · Bob Ross · Paquete de Entrada y Question Forge

> **ACTUALIZACIÓN 19-11-2026:** este archivo conserva contexto de etapas anteriores. **Para el estado ACTUAL y los próximos pasos usa primero [HANDOFF_2026-11-19.md](HANDOFF_2026-11-19.md) y copia [PROMPT_NEXT_CHAT_2026-11-19.md](PROMPT_NEXT_CHAT_2026-11-19.md).** PR #12, #14 y #15 ya fusionados en `main`; DR-01/02/03 recibidos y archivados como normalizaciones estructuradas, no hallazgos validados ni textos literales. Las secciones inferiores sobre «próxima conversación» deben leerse como contexto histórico, no como estado actual.

**Leer este archivo primero en una conversación nueva. Es autocontenido.**

**ARQUITECTURA INTEGRADA:** PR #11 (núcleo compartido) y PR #5 (episodio base) se fusionaron en `main` el 18 de noviembre de 2026. El PR #10 **también está fusionado en `main`** e incorpora este Paquete de Entrada y la guía V3. La skill canónica está en `discovery_labs/shared/skills/question-forge/SKILL.md`, los 24 modelos en `discovery_labs/shared/model_catalog/MODEL_SET.md` y los validadores en `discovery_labs/shared/validators/`. No mantener copias de la skill, catálogo o plantillas por episodio. El documento `entry_pack/MODEL_FIT_BOB_ROSS.md` conserva solo criterios de Bob Ross. Revisar la versión actual de `main` antes de trabajar: la guía científica requiere aprobación humana, independientemente del merge de código.

## 1) Qué es y qué se quiere
Proyecto educativo **AI Discovery Labs**, dentro del repositorio público [jcval94/DataCollectionMov](https://github.com/jcval94/DataCollectionMov). Se busca convertir 86 fuentes en investigaciones científicas memorables, reproducibles y aptas para clases de ~45 minutos, con una futura adaptación audiovisual.

El caso piloto es Bob Ross / *The Joy of Painting*. La investigación debe contar **la historia real de Bob Ross**, no solo contar ocurrencias de TREE. Las preguntas deben emerger de biografía, historia, hipótesis externas y hallazgos medidos, incluidos subproblemas de segundo y tercer orden. Las visualizaciones deben transmitir evidencia, con hover/focus de episodios y pinturas solo si los derechos lo permiten.

**PREFERENCIA DE PROCESO DEL USUARIO — mantener en todos los episodios:**
1. **Fase 0:** Paquete de Entrada (Deep Research, muestras, metadatos, preguntas profundas, modelo + estadística por pregunta, fuentes, planificación y visualizaciones).
2. **Fase 1:** guía HTML científica/técnica **con UN SOLO bloque integrado de preguntas**; requiere aprobación explícita de versión/commit.
3. **Fase 2:** HTML de storytelling audiovisual/guion/storyboard **solo si Fase 1 se aprobó**; requiere segunda aprobación explícita.
4. **Fase 3:** producción/render del video **solo tras aprobar Fase 2**.

No crear video, intro, Remotion, voz o storyboard antes de aprobación.

## 2) Estado actual del repositorio
- PR base del episodio: [#5 — Bob Ross aislado](https://github.com/jcval94/DataCollectionMov/pull/5), rama `feat/bob-ross-discovery-episode-only`, contiene CSV, `run.py`, clustering, HTML interactivo, QA y materiales de clase.
- PR del Paquete de Entrada y skill: [#10 — entrada/Question Forge](https://github.com/jcval94/DataCollectionMov/pull/10), rama `feat/bob-ross-entry-pack-question-forge`, **fusionado en `main` después de resolver conflictos y preservar pruebas heredadas**. No es necesario trabajar en ramas anteriores.
- Carpeta única autorizada para modificaciones de Bob Ross: `discovery_labs/episodes/bob-ross/`. Nunca tocar otras carpetas, otros casos, `.github/workflows`, `mvp-ds-course` ni cambios locales ajenos sin permiso.
- El HTML actual del episodio (`episode.html`) y el archivo `questions.json` mantienen **seis entradas heredadas de UI**, que NO son el banco editorial canónico. No borrarlos sin adaptar la interfaz y verificar tests. Para ciencia/guía usar `entry_pack/questions_master.json`.

## 3) Archivos MD y orden de lectura obligatorio

1. **`entry_pack/START_HERE_NEW_CHAT.md`** — este handoff, decisiones y acciones.
2. **`entry_pack/README.md`** — índice del Paquete de Entrada y estados.
3. **`discovery_labs/shared/skills/question-forge/SKILL.md`** — **habilidad GENERALIZABLE V2**. Obligatoria cuando se crean o revisan preguntas.
4. **`discovery_labs/shared/templates/ENTRY_PACK_TEMPLATE.md`** — plantilla para los otros 85 datasets y futuros episodios.
5. **`entry_pack/QUESTIONS_MASTER.md`** — **único bloque editorial** de 14 investigaciones de Bob Ross. Preguntas O1/O2/O3, modelo y ejercicio estadístico por cada una. Versión máquina: `questions_master.json`.
6. **`discovery_labs/shared/model_catalog/MODEL_SET.md`** — catálogo de **24 modelos/familias** con idoneidad, límites y pruebas estadísticas. NO entrenar en Fase 0.
7. **`entry_pack/DEEP_RESEARCH_PROMPTS.md`** — DR-01…DR-04 con síntesis DR-05 (historia y salud, datos/cronología, mitos, visualización/derechos).
8. **`entry_pack/CONTEXT_CLAIMS.md`** — registro externo y cronología **DISPUTADA** del diagnóstico de linfoma.
9. **`entry_pack/RESEARCH_PLAN.md`** — secuencia de investigación de Fase 1, metodología y gates.
10. **`entry_pack/VISUAL_DESIGN.md`** — gráficos fuertes, matrices 31×12, outliers, cluster explorer con preview condicional y QA.
11. **`entry_pack/PROMPT_FASE1_V2.md`** — prompt para iniciar Fase 1 con otra IA.
12. **`entry_pack/QA_PACK_STATUS.md`** — validaciones estáticas y lo que falta probar. **`entry_pack/validate_pack.py`** — comprobaciones estáticas del paquete, sin modelos entrenados. **`research_guide.html`** — primera guía científica V3 **ya incorporada al repo**, con UNA sección de 14 preguntas y enfermedad visible; pendiente de aprobación.
13. Documentos de apoyo históricos: `entry_pack/QUESTION_ARCS.md` y `entry_pack/question_graph.json` son **borradores de ideas anteriores** para trazabilidad; **no son un segundo banco de preguntas**.
14. Archivos de datos: `entry_pack/metadata.json`, `entry_pack/sample_raw.csv` (13 filas originales), `entry_pack/sample_features.csv` (mismas filas, 12 motivos). Los 13 ejemplos **no** son una muestra representativa ni deben usarse para métricas poblacionales.

## 4) Evidencia y límites técnicos
- Fuente original: FiveThirtyEight/Walt Hickey, 403 episodios etiquetados (S01–S31), 69 columnas (EPISODE, TITLE, 67 indicadores binarios), CSV de 66,315 bytes, hash SHA-256 `42045c8b8aaa8296095d6b294927fb9d0f73a57259f59b560c375844c0fe01cf`. CC BY 4.0 **para datos, no para pinturas ni videos**.
- 381 episodios sin invitados, 22 con GUEST. Entre anfitrión: 345 con TREE/TREES, 36 sin esos motivos; 150 con montaña y 48 de esos sin nieve. Los conteos son evidencia descriptiva **ya presente en el episodio**, no producto de entrenamientos nuevos.
- `SNOWY_MOUNTAIN` activa montaña Y nieve; dependencia por construcción. Estilo, creatividad, emoción, precio, audiencia, enfermedad, fechas reales de grabación y color **NO son variables del CSV**.
- Salud: Ross murió de linfoma en 1995. **Las fechas secundarias del diagnóstico discrepan**: una fuente señala primavera de 1994, otra sugiere poco después de la muerte de Jane (1992). **No** se puede atribuir cambio de estilo a enfermedad ni poner línea de diagnóstico sobre un gráfico por temporada sin resolver cronología y producción. Ver `CONTEXT_CLAIMS.md`.
- NPR describe tres versiones preparadas para episodios; AP reportó siete pinturas para una temporada 32 inconclusa. Son contexto de cobertura, **no** nuevas filas equivalentes del CSV.

## 5) CORRECCIÓN editorial solicitada por el usuario

**Problema anterior:** el HTML mostraba seis preguntas simples en la sección 02 y las profundas en otra llamada 02B. La enfermedad quedaba como una nota tardía; no se proponía modelo ni ejercicio estadístico por pregunta.

**Corrección obligatoria:**
- El nuevo HTML Fase 1 debe mostrar **solo una sección de preguntas**, alimentada por `questions_master.json`, donde conviven TODAS las rutas profundas. Nada de «2B» ni «seis básicas + doce avanzadas».
- Las seis rutas antiguas solo son puntos de entrada que se **integran como subpreguntas O1**, experimentos o rutas dentro del banco, con tabla de trazabilidad en `QUESTIONS_MASTER.md`.
- La enfermedad debe aparecer **en el cuerpo principal** como `BR-01`, con metodología y fuentes contrastadas. No como «Bob enfermó y empezó a pintar diferente»: eso no está demostrado.
- **Cada pregunta BR-01…BR-14 lleva al menos un modelo Y un ejercicio estadístico independiente**, incluyendo qué, por qué, dónde, datos, baseline, validación y limitaciones.
- **No ejecutar ni entrenar** aún esos modelos: en Fase 0 solo se diseñan. LSTM, RL, Optuna o riesgo colectivo no se fuerzan en un dataset insuficiente.
- O2/O3 se escriben como hipótesis condicionales hasta que haya evidencia de O1/O2.

## 5 bis) Nuevas reglas permanentes para todos los episodios

**Misión:** perseguir insights **increíbles, originales e innovadores** de cada dataset, solo cuando los sustenten fuentes, contrastes y análisis reproducibles. No fabricar una «sorpresa» ni un impacto no medible.

**Tres preguntas explícitas que deben responder la investigación y el documento científico:**

- **CÓMO:** dataset, variables, grano, pipeline, modelo y prueba estadística independiente, sensibilidad y reproducción.
- **POR QUÉ:** relevancia histórica/científica, elección de método, hipótesis rivales, límites de explicación.
- **PARA QUÉ:** qué cambia en la comprensión, qué decisión posibilita o qué experimento sigue.

**HTML inicial y evolución:** comenzar con un párrafo de contexto general y estructura: contexto → misión → fuente/límites → un único índice de **O1** → métodos/espacios de evidencia → análisis crítico → utilidad → reproducción/versiones. O2/O3 permanecen **diseños condicionales en JSON y Markdown**, sin presentarlas de entrada como preguntas activas del HTML. Medir O1 + contrastar DR temprano + checkpoint DR-05a antes de publicar O2; medir O2 + comprobar hipótesis rival antes de publicar O3. Mantener historial de versión, ID padre, triggers, evidencias y resultados nulos. **No reescribir retroactivamente un resultado sin bitácora**. El HTML V3 existente es una instantánea de preguntas que aún debe adaptarse a esta presentación progresiva.

**Cinco frentes, no cinco Deep Research simultáneos:** primero **DR-01/02/03**, profundizar **DR-04** después de resultados O1 e insights seleccionados (triage temprano de licencias), usar **DR-05** como síntesis provisional tras O1 y cierre al final. La pauta está fijada en `discovery_labs/shared/skills/question-forge/SKILL.md`, `discovery_labs/shared/templates/ENTRY_PACK_TEMPLATE.md`, `entry_pack/DEEP_RESEARCH_PROMPTS.md` y `entry_pack/RESEARCH_PLAN.md`.

**Gobernanza:** estos son requisitos escritos para la **siguiente versión** del HTML. No equiparar su documentación con la ejecución de Deep Research, la aprobación científica ni la autorización del storyboard/video.

## 6) Qué hacer en la próxima conversación
**Si la petición es continuar Fase 0:** revisar y terminar skill/entrada, QA de JSON y enlaces, confirmar el PR y estado, sin crear nuevos modelos entrenados.

**Si la petición es construir Fase 1:** ejecutar Deep Research con fuentes verificables, preprocesamiento, análisis, modelos apropiados **solo si la nueva petición lo autoriza**, pruebas estadísticas, enriquecer dataset y producir `research_guide.html` con un bloque único de preguntas, visualizaciones fuertes, modos narrativo/técnico, derechos revisados y QA visual. **Detenerse antes de Fase 2.**

Comandos de lectura/QA que puedes ejecutar desde raíz de repo (sin modificar otras carpetas):
```bash
git status --short
python discovery_labs/episodes/bob-ross/run.py --check
python -m unittest discover -s discovery_labs/episodes/bob-ross/tests -v
node discovery_labs/episodes/bob-ross/qa_static.cjs # opcional si Node
```

## 7) Prompt literal para copiar en conversación nueva

> Continúa AI Discovery Labs / Bob Ross desde el Paquete de Entrada de la rama `main` del repositorio `jcval94/DataCollectionMov` (PRs #5, #10 y #11 fusionados). Antes de ejecutar nada, lee `discovery_labs/episodes/bob-ross/entry_pack/START_HERE_NEW_CHAT.md`, `README.md`, `discovery_labs/shared/skills/question-forge/SKILL.md`, `QUESTIONS_MASTER.md`, `discovery_labs/shared/model_catalog/MODEL_SET.md`, `DEEP_RESEARCH_PROMPTS.md`, `CONTEXT_CLAIMS.md`, `RESEARCH_PLAN.md`, `VISUAL_DESIGN.md` y las muestras/metadatos. La regla editorial es una única lista integrada de preguntas profundas, con O1/O2/O3 y al menos un modelo + un ejercicio estadístico diseñado por pregunta. La misión es descubrir insights innovadores verificables y explicar siempre CÓMO, POR QUÉ y PARA QUÉ. El HTML inicial debe abrir con un párrafo de contexto y mostrar solo O1; O2 se incorporan después de responder O1 y ejecutar DR-01/02/03 con DR-05a, y O3 tras obtener evidencia O2. Diferir DR-04 profundo hasta seleccionar insights y cerrar DR-05b al final. No entrenes modelos ni hagas video si estoy pidiendo solo paquete/planeación. Incluye enfermedad como hipótesis histórica con fechas disputadas, sin causalidad inventada. Trabaja únicamente en la carpeta del episodio, preserva cambios concurrentes y reporta pruebas y pendientes. Las Fases 2 y 3 requieren mis aprobaciones explícitas.

## 8) Definición de terminado de esta etapa
Paquete autocontenido, skill transferible, 14 preguntas integradas, modelo + estadística por pregunta, 24 modelos catalogados, fuente y contradicciones registradas, plan visual potente, metadatos/muestra genuinos, archivos accesibles y PR listo para revisión. **NO afirmar que Deep Research completo, modelos o guía definitiva ya se ejecutaron.**

**Última regla:** investigación científica primero; después de aprobarla, guion audiovisual; después de aprobarlo, video.
