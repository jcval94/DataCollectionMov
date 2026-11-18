# AI Discovery Labs — Paquete de Entrada 001 (Bob Ross)

> **Objetivo:** conocer el caso *antes* de preparar el informe científico, construir preguntas profundas y descubrir qué evidencia externa falta. **No es el guion de video.**

## Contenido del paquete
| Recurso | Para qué sirve |
|---|---|
| [DEEP_RESEARCH_PROMPTS.md](DEEP_RESEARCH_PROMPTS.md) | Cuatro investigaciones especializadas y una síntesis adversarial; guiones listos para IA con navegación |
| [skills/question-forge/SKILL.md](skills/question-forge/SKILL.md) | Skill reusable de generación, depuración y priorización de preguntas O1→O2→O3 |
| [QUESTION_ARCS.md](QUESTION_ARCS.md) | 12 líneas prometedoras: vida, evolución, outliers multiescala, mitos, invitados, clustering, obra excluida |
| [question_graph.json](question_graph.json) | Grafo estructurado de 33 nodos (12 O1, 12 O2 y 9 O3) con dependencias y estados |
| [sample_raw.csv](sample_raw.csv) | 13 filas originales reales con 69 columnas; muestra intencional, NO representativa |
| [sample_features.csv](sample_features.csv) | Las mismas 13 filas con temporada, invitado y doce familias binarias explicadas |
| [metadata.json](metadata.json) | Procedencia, hash, grano, cobertura, formato, lagunas, licencias y vías de enriquecimiento |
| [RESEARCH_PLAN.md](RESEARCH_PLAN.md) | Lotes de investigación, métodos, dependencias, QA y contrato del primer HTML |
| [VISUAL_DESIGN.md](VISUAL_DESIGN.md) | Ocho figuras de alta calidad, explorador de clusters, tarjeta hover/focus y políticas de imágenes |
| [PROMPT_FASE1_V2.md](PROMPT_FASE1_V2.md) | Encargo para el agente local: ejecutar Deep Research, evaluar preguntas y enriquecer **únicamente** el HTML científico |

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
4. Aplica `question-forge`: rankea arcos, elige 3–5 y realiza pruebas reales.
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
**PAQUETE DE ENTRADA = PREPARADO** (instrumentos, no investigación Deep Research ejecutada). **Guía científica V2 = pendiente de investigación, reejecución y aprobación**. **Storytelling audiovisual = BLOQUEADO**. **Video = BLOQUEADO**.

Ninguna fuente externa, pregunta condicional, agrupamiento o visualización de derechos dudosos debe transformarse en conclusión «verificada» por mera presencia en este paquete.
