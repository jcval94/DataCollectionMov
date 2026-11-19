# AI Discovery Labs — Paquete de Entrada 001 (Bob Ross)

> **CONTINUIDAD (19-11-2026):** la ruta vigente para retomar Bob Ross es [HANDOFF_2026-11-19.md](HANDOFF_2026-11-19.md) y el [prompt para un nuevo chat](PROMPT_NEXT_CHAT_2026-11-19.md). Las tres investigaciones DR-01/02/03 ya se archivaron bajo [research_received/](research_received/README.md) en PR #15 (fusionado). PR #12 y #14 también se fusionaron; sus entregas son QA y metodología, **no resultados científicos aprobados**.

> **Infraestructura compartida integrada en `main` (PR #11):** usar [Question Forge v2.1](../../../shared/skills/question-forge/SKILL.md), [catálogo único de 24 modelos](../../../shared/model_catalog/MODEL_SET.md) y [plantilla general](../../../shared/templates/ENTRY_PACK_TEMPLATE.md). Este episodio conserva solo preguntas, datos y criterios específicos. [MODEL_FIT_BOB_ROSS.md](MODEL_FIT_BOB_ROSS.md) documenta sus límites. **No existen copias locales de la skill ni del catálogo.**


> **Objetivo:** conocer el caso *antes* de preparar el informe científico, construir preguntas profundas y descubrir qué evidencia externa falta. **No es el guion de video.**

## INICIO en nueva conversación

**Lee primero [START_HERE_NEW_CHAT.md](START_HERE_NEW_CHAT.md).** Contiene el contexto autocontenido, ramas, PR, instrucciones de no modificar fuera del episodio, estado exacto y un prompt literal. Para generalizar a nuevos episodios: [Plantilla general](../../../shared/templates/ENTRY_PACK_TEMPLATE.md).

## Objetivo y nuevo protocolo editorial

**AI Discovery Labs existe para descubrir insights increíbles e innovadores de cada dataset, siempre demostrables, reproducibles y útiles para pensar mejor.** Un resultado sorprendente solo cuenta si resiste comparaciones, pruebas adversariales y explicaciones alternativas; también es un descubrimiento demostrar que un supuesto era falso.

Para cada pregunta, experimento y hallazgo explicar tres dimensiones explícitas:

- **CÓMO** se investiga y reproduce: fuente, grano, limpieza, modelo, prueba estadística, contraste, incertidumbre.
- **POR QUÉ** importa y es verosímil: contexto, método, hipótesis rival y limitaciones.
- **PARA QUÉ** sirve: cambio en nuestra comprensión, decisión informada o experimento siguiente.

**El HTML inicial tiene un párrafo de contexto general al comienzo y una estructura estable** (contexto → misión → datos/límites → índice único O1 → evidencia → interpretación/utilidad → reproducibilidad/aprobación). Debe **actualizarse a medida que se investiga**: primero O1; solo después de medir O1 y revisar DR-01/02/03 más DR-05a se agregan O2 justificadas, y solo después de ejecutar O2 se incorporan O3 respaldadas. El banco JSON/MD conserva O2/O3 como **diseños internos condicionales**, no como preguntas activas desde el día uno. La V3 actual es preliminar y no cumple todavía esta visualización progresiva.

**Deep Research no todo a la vez:** DR-01 historia, DR-02 datos y DR-03 antecedentes son tempranos; DR-04 visual/derechos se profundiza **al seleccionar insights** (triage de licencias desde el principio); DR-05 es un checkpoint de síntesis tras O1 y un cierre final, no cinco búsquedas obligatoriamente paralelas. Ver [`DEEP_RESEARCH_PROMPTS.md`](DEEP_RESEARCH_PROMPTS.md) y [`RESEARCH_PLAN.md`](RESEARCH_PLAN.md).

## Contenido canónico

| Recurso | Función |
|---|---|
| [START_HERE_NEW_CHAT.md](START_HERE_NEW_CHAT.md) | **Handoff** a otra conversación sin contexto |
| [Plantilla general](../../../shared/templates/ENTRY_PACK_TEMPLATE.md) | **Plantilla general** para los otros 85 casos y futuros |
| [Question Forge v2.1](../../../shared/skills/question-forge/SKILL.md) | **Skill reutilizable v2**: preguntas de 3 órdenes, un modelo y un ejercicio estadístico por pregunta |
| [QUESTIONS_MASTER.md](QUESTIONS_MASTER.md) | **Único bloque editorial de 14 investigaciones**; incluye enfermedad y trazabilidad de las seis rutas antiguas |
| [questions_master.json](questions_master.json) | Única fuente estructurada de preguntas; **deberá** alimentar la guía HTML integrada cuando se automatice la Fase 1 (V3 es snapshot estático) |
| [Catálogo de 24 modelos](../../../shared/model_catalog/MODEL_SET.md) | 24 modelos/familias con adecuación, ejercicios estadísticos, validación, restricciones y ubicación |
| [DEEP_RESEARCH_PROMPTS.md](DEEP_RESEARCH_PROMPTS.md) | DR-01…DR-04 y DR-05 de síntesis |
| [CONTEXT_CLAIMS.md](CONTEXT_CLAIMS.md) | Evidencia externa y fechas contradictorias sobre enfermedad: NO atribución causal |
| [RESEARCH_PLAN.md](RESEARCH_PLAN.md) | Lotes y aprobación Fase 1 |
| [VISUAL_DESIGN.md](VISUAL_DESIGN.md) | Visualizaciones, cluster hover/focus, derechos y QA |
| [metadata.json](metadata.json) | Metadatos verificables y faltantes |
| [sample_raw.csv](sample_raw.csv) | 13 registros originales con 69 columnas |
| [sample_features.csv](sample_features.csv) | Las mismas 13 filas derivadas con 12 familias |
| [PROMPT_FASE1_V2.md](PROMPT_FASE1_V2.md) | Encargo local de guía científica y gates |
| [validate_pack.py](validate_pack.py) | Comprobaciones sin entrenar modelos de una sola lista y 14 contratos modelo/estadística |
| [QA_PACK_STATUS.md](QA_PACK_STATUS.md) | Validaciones estáticas realizadas y pruebas todavía pendientes |
| [../research_guide.html](../research_guide.html) | Primera guía HTML V3, con las 14 preguntas en **una sola sección**; **pendiente de aprobación** |

**Trazabilidad histórica, NO segundo banco:** [QUESTION_ARCS.md](QUESTION_ARCS.md) y [question_graph.json](question_graph.json) conservan 12 líneas previas y 33 nodos; se sustituyen editorialmente por `QUESTIONS_MASTER.*`. Las seis preguntas antiguas del `../questions.json` sirven a la interfaz actual, no se deben duplicar en la nueva guía.

**Regla central:** la guía HTML debe tener un **solo bloque principal de preguntas**. Ni seis simples por un lado y nuevas en «2B», ni enfermedad relegada al final. Cada una de las 14 preguntas incluye un modelo y una prueba estadística planificados. **NO se han entrenado ni ejecutado.**

## Qué cambió
El primer inventario de Bob Ross contenía preguntas que podían resolverse mediante consultas sencillas. **Ahora las consultas son piezas de evidencia, no la investigación entera.**

- El episodio tiene que contar **la historia documentada de Bob Ross** y su trabajo a lo largo de la serie.
- La **salud** es un contexto biográfico investigable; no se permite atribuirle cambios estilísticos sin pruebas sólidas.
- El tiempo requiere distinguir **orden de temporada, emisión y grabación**; el CSV no tiene fechas exactas.
- Las preguntas de segundo orden nacen de resultados O1 comprobados y las de tercer orden refutan, explican o comparan O2: ninguna debe presentarse como hallazgo anticipado.
- Los outliers se estudian a **tres escalas**: episodio, temporada y era/cohorte; las supuestas anomalías necesitan explicación rival y pruebas de sensibilidad.
- Las «creencias populares» requieren una fuente que documente efectivamente la creencia; de lo contrario son provocaciones.
- Las pinturas en tooltips requieren **derechos comprobados**; cuando falten, usar tarjetas de atributos y enlaces a sus páginas originales, con interacción para mouse, teclado y móvil.

## Qué sí sabemos de la fuente original
- FiveThirtyEight / Walt Hickey, 403 episodios codificados.
- CSV de 66,315 bytes, 69 columnas: EPISODE, TITLE y 67 etiquetas binarias.
- 381 episodios sin GUEST y 22 con GUEST.
- Entre los 381: 345 tienen TREE/TREES, 36 no; entre 150 con montaña, 48 no tienen nieve codificada.
- Temporadas ordenadas S01–S31; **no** usar ese código como fecha histórica exacta.
- Datos bajo CC BY 4.0, **no** las reproducciones ni los videos.

## Cómo utilizarlo con otra IA
1. Carga este paquete y la carpeta padre del episodio (CSV íntegro, scripts y figuras).
2. Ejecuta DR-01, DR-02, DR-03 y DR-04 con referencias rastreables.
3. Ejecuta DR-05 después de reconciliar hechos y completar la matriz de afirmaciones.
4. Aplica `question-forge`: utiliza solo `QUESTIONS_MASTER.*`, prioriza 3–5 y diseña un modelo + ejercicio estadístico por ruta. No ejecutar entrenamientos en Fase 0.
5. Actualiza `research_guide.html` **con evidencia verificada, gráficos vinculados al snapshot y nivel técnico**, no solo texto narrativo.
6. Detente con estado `PENDIENTE_APROBACION_CIENTIFICA`. No crear storytelling de video ni producción audiovisual.

## Verificación de integridad
Los CSV del paquete se extrajeron de la copia inmutable del episodio (`../data/elements-by-episode.csv`). La muestra incluye diferentes temporadas y dos invitados para ilustrar la diferencia de grupos. **Nunca calcular porcentajes de población sobre las 13 filas**. Para resultados usar siempre las 403 filas originales y aplicar denominadores explícitos.

## Ejemplos de fuentes contextuales para iniciar Deep Research
- [NPR/KPBS (2016)](https://www.kpbs.org/news/2016/08/28/the-real-bob-ross-meet-the-meticulous-artist): producción, biografía y preparación de obras.
- [Outside / Walt Hickey](https://www.outsideonline.com/podcast/bob-ross-strategies-survival/): investigación estadística y la vida privada.
- [AP (2024)](https://apnews.com/article/bob-ross-painting-unfinished-season-nichola-hankins-cd50203eb6b3cf4f1893364cfae472be): siete pinturas para una temporada 32 inconclusa.
- [jwilber/Bob_Ross_Paintings](https://github.com/jwilber/Bob_Ross_Paintings): metadatos de pinturas, temporada, episodio, paletas; verificar derechos.
- [Wiley (2014)](https://doi.org/10.1002/meet.2014.14505101084): trabajo previo de visualización sobre datos de Bob Ross.

## Estado
**PAQUETE DE ENTRADA = PREPARADO PARA REVISIÓN** (skill V2, 14 preguntas profundas, 24 modelos y planes estadísticos; no hay nuevos modelos entrenados ni investigación Deep Research completa). **Guía científica V3 = pendiente de consolidación, investigación, reproducción y aprobación**. **Storytelling audiovisual = BLOQUEADO**. **Video = BLOQUEADO**.

Ninguna fuente externa, pregunta condicional, agrupamiento o visualización de derechos dudosos debe transformarse en conclusión «verificada» por mera presencia en este paquete.
