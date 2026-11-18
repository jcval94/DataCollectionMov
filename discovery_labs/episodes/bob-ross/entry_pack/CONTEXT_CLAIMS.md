# Registro inicial de afirmaciones externas — Bob Ross

**Fecha de revisión:** 2026-11-18. **Alcance:** hipótesis históricas útiles para diseñar la investigación. La investigación documental completa DR-01…DR-05 todavía no está ejecutada, por lo que este registro no autoriza atribuciones causales.

| ID | Afirmación / tensión | Fuente comprobable | Estado editorial | Uso y límite |
|---|---|---|---|---|
| H01 | La serie televisiva tuvo 403 episodios distribuidos en 31 temporadas (1983–1994). | [FiveThirtyEight, Walt Hickey](https://github.com/fivethirtyeight/data/tree/4c1ff5e3aef1816ae04af63218015066e186c147/bob-ross); [AP 2024](https://apnews.com/article/cd50203eb6b3cf4f1893364cfae472be) | SOURCE_SUPPORTED | Grano episodio; no cuadros físicos ni fechas de grabación |
| H02 | NPR informa que Ross preparaba tres versiones del cuadro por episodio: referencia, filmación y libro. | [NPR 2016, republicado por NCPR](https://www.northcountrypublicradio.org/news/npr/490923502/the-real-bob-ross-meet-the-meticulous-artist-behind-those-happy-trees) | REPORTED_NEEDS_CORPUS_RECONCILIATION | No multiplicar filas por tres; versiones no verificadas en el CSV |
| H03 | Associated Press informó sobre siete obras preparadas para una temporada 32 no producida por Ross. | [AP, 10 mayo 2024](https://apnews.com/article/cd50203eb6b3cf4f1893364cfae472be) | SOURCE_SUPPORTED | Frontera de selección; no incorporarlas como episodios observados |
| H04 | Bob Ross murió el 4 de julio de 1995 por complicaciones de linfoma. | [NPR 2016](https://www.northcountrypublicradio.org/news/npr/490923502/the-real-bob-ross-meet-the-meticulous-artist-behind-those-happy-trees), [People 2024](https://people.com/bob-ross-death-what-to-know-7558507) | SOURCE_SUPPORTED | Contexto histórico, no resultado estadístico del dataset |
| H05 | La fecha precisa del diagnóstico es **inconsistente entre relatos secundarios**: Outside sitúa el diagnóstico en primavera de 1994; una reseña de documental en Washington Post lo ubica semanas después de la muerte de Jane, que otros relatos sitúan en 1992. | [Outside, episodio del pódcast](https://www.outsideonline.com/podcast/bob-ross-strategies-survival/); [Washington Post 2021](https://www.washingtonpost.com/arts-entertainment/2021/08/27/bob-ross-netflix-documentary/); [People, Jane murió en 1992](https://people.com/bob-ross-death-what-to-know-7558507) | **DISPUTED — REQUIRES PRIMARY EVIDENCE** | **NO** dibujar una línea vertical en temporadas como «fecha del diagnóstico» sin reconciliación y calendario de filmación |
| H06 | Hay testimonios de que Ross siguió grabando pese a la enfermedad. | [Washington Post 2021](https://www.washingtonpost.com/arts-entertainment/2021/08/27/bob-ross-netflix-documentary/); [Outside](https://www.outsideonline.com/podcast/bob-ross-strategies-survival/) | REPORTED_NOT_MEASURED | No asumir cuál episodio se pintó durante enfermedad |
| H07 | La condición clínica o tratamiento modificó la paleta, creatividad o «tristeza» de su obra. | **No demostrado por el CSV de 67 etiquetas** | **NOT_SUPPORTED** | Es una pregunta de investigación; NO es una conclusión ni puede probarse sin diseño causal y fuentes externas |
| H08 | Los «árboles felices» son parte documentada de su imagen cultural. | [NPR 2016](https://www.northcountrypublicradio.org/news/npr/490923502/the-real-bob-ross-meet-the-meticulous-artist-behind-those-happy-trees) | SOURCE_SUPPORTED | El arquetipo es un encuadre editorial; prevalencia del motivo sí se mide en CSV |
| H09 | Paletas e imágenes podrían enriquecer la investigación. | [jwilber/Bob_Ross_Paintings](https://github.com/jwilber/Bob_Ross_Paintings) | TO_VERIFY_JOIN_LICENSE | Campos, disponibilidad, licencias, fechas y correspondencia por episodio pendientes |

## Protocolo para DR-01 (enfermedad como hipótesis, no como hecho causal)

1. Investigar cuándo murió Jane, cuándo Bob recibió diagnóstico, qué variantes hay, fuentes primarias/entrevistas, y **grado de precisión temporal**. No hacer un «promedio» de fechas contradictorias.
2. Determinar el calendario real de grabaciones de cada episodio y cuándo fue emitido; si falta, usar SOLO orden ordinal de temporada sin marcador clínico.
3. Ejecutar primero análisis descriptivo de motivos/paletas/complexidad **sin** consultar el evento clínico. Registrar conclusiones preespecificadas o riesgos de análisis post-hoc.
4. Solo después contrastar si existe coincidencia temporal verificable y explicaciones rivales de producción, grabación anticipada, invitados, técnica, iluminación, disponibilidad de corpus y medición.
5. Si la atribución no es identificable, titular la sección **«¿Cambió algo hacia el final? Lo que no podemos atribuir»**. No inferir sufrimiento ni estado emocional de las pinturas.

## Esquema de evidencia que se debe completar

Cada fuente/afirmación debe registrar: `claim_id`, `claim`, `published_at`, `event_at`, `recorded_at_if_known`, `type`, `source_url`, `excerpt_short`, `confidence`, `contradicting_claim_ids`, `research_questions`, `last_verified`. `PENDING` para fechas o cobertura desconocidas.

**Nota metodológica:** estas fuentes apoyan preguntas históricas y cronologías, pero no equivalen a variables observadas en los 403 episodios. La validación de inferencia se hace más adelante en Fase 1; este Paquete de Entrada **solo diseña**.
