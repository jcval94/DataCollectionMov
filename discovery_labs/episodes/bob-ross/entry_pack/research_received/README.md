# AI Discovery Labs · Bob Ross — DR-01, DR-02 y DR-03 recibidos

**Estado de integración:** archivo incorporado a `main` mediante [PR #15](https://github.com/jcval94/DataCollectionMov/pull/15), fusionado el 19-11-2026. Consultar el [handoff actualizado](../HANDOFF_2026-11-19.md) y el [prompt para conversación nueva](../PROMPT_NEXT_CHAT_2026-11-19.md) antes de continuar. La procedencia sigue siendo material recibido y normalizado, **no transcripción literal ni prueba científica validada**.

> **Archivado en GitHub:** 19 de noviembre de 2026.  
> **Estado:** recepción **completa de tres investigaciones en la conversación**, con **archivo estructurado (no transcripción literal íntegra)** de sus hallazgos, fuentes, tablas e hipótesis más relevantes.  
> **Proveniencia:** textos aportados por el usuario en tres mensajes sucesivos del chat.  
> **Aprobación científica:** `NOT_REVIEWED`; no existe evidencia de que los tres informes hayan ejecutado pruebas inferenciales.  
> **Regla de no sobrescritura:** preservar entrada histórica y editar bancos canónicos únicamente después de conciliación científica y autorización de fase.

## Qué se ha guardado

| Investigación | Informe archivado | Anexos estructurados |
|---|---|---|
| **DR-01 — biografía e historia** | [DR-01_BIOGRAFIA_HISTORIA.md](DR-01_BIOGRAFIA_HISTORIA.md) | [DR-01_timeline_events.csv](DR-01_timeline_events.csv): **22 hitos** E01–E22 |
| **DR-02 — arqueología y enriquecimientos** | [DR-02_ARQUEOLOGIA_MULTIFUENTE.md](DR-02_ARQUEOLOGIA_MULTIFUENTE.md) | [DR-02_source_inventory.csv](DR-02_source_inventory.csv): **11 fuentes** |
| **DR-03 — mitos, antecedentes e hipótesis** | [DR-03_MITOS_ANTECEDENTES_HIPOTESIS.md](DR-03_MITOS_ANTECEDENTES_HIPOTESIS.md) | [DR-03_myths_claims.csv](DR-03_myths_claims.csv): **13** MC01–MC13; [DR-03_antecedents.csv](DR-03_antecedents.csv): **8** ANT01–ANT08; [DR-03_rival_explanations.md](DR-03_rival_explanations.md): R1–R5; [DR-03_questions_to_test.json](DR-03_questions_to_test.json): **10** H1–H10 |

**Integridad:** [MANIFEST.json](MANIFEST.json) registra SHA de objeto Git, longitud de contenido, tipo y recuento de cada archivo. Los ficheros están separados del banco editorial `entry_pack/QUESTIONS_MASTER.md` y `questions_master.json`.

## Alcance exacto del archivo y límites

Los documentos Markdown y anexos de esta carpeta **son normalizaciones y resúmenes extensos del material recibido**, **no una captura byte a byte de los mensajes completos**. Conservaron argumentos principales, procedencia, contradicciones, diseños científicos y claves necesarias, pero parte de la prosa original y algunas columnas secundarias del CSV/JSON enviado se condensaron. **Los textos literales íntegros siguen en los tres mensajes originales de esta conversación**. Si se requiere archivo literal auditable en GitHub, transferir los originales como archivos adjuntos o fuentes de texto para evitar errores de transcripción.

Esto NO acredita que las URLs se hayan abierto ni que los calificativos `VERIFIED`, `AVAILABLE` o `REFUTED` sean comprobaciones de este archivado. En varias tablas, dichos rótulos están explícitamente marcados **as_received**. El acceso al repo que falló en el entorno de los investigadores **no significa** que el GitHub conectado de esta conversación sea inaccesible.

Los informes contienen puntos a conciliar antes de integrar conocimiento: 3,224 vs 3,221 vs 3,324 etiquetas; autores invitados 22 vs listados externos; cronología de diagnóstico discutida; fecha emisión ≠ fecha grabación; licencias de las imágenes; variables PERSON/CHIMNEY no necesariamente existentes; etiquetado de la obra que puede corresponder a versión comercial/book distinta de TV; disponibilidad e idoneidad de H5/H7 que requieren imágenes protegidas.

## Qué NO se hizo

- No se realizaron Deep Research adicionales, navegación de fuentes externas ni auditoría de los hechos.
- No se entrenaron modelos, ejecutaron contrastes estadísticos ni comprobaron hipótesis.
- No se fusionaron H1–H10 con las 14 preguntas canónicas BR-01–BR-14; **no son un segundo banco oficial**.
- No se modificaron datos, scripts, HTML V3, catálogo general, storytelling ni video.
- No se realizaron automáticamente análisis de O1 y las O2/O3 del material recibido siguen `CONDICIONAL`.

## Siguiente fase científica, solo cuando proceda

1. Reconciliar DR-01/02/03 en una **matriz de evidencias** con fuente, tipo de fuente, confianza y conflictos sin inventar certeza.
2. Ejecutar QA fuente sobre CSV original y contrastar las cifras discordantes (tags, invitados, duplicados, incompletos).
3. Determinar datasets secundarios **legalmente utilizables** y coste de cada hipótesis; separar H5/H7 dependientes de imágenes.
4. Cruzar hipótesis H1–H10 con BR-01–BR-14 sin crear banco paralelo, elegir 3–5 investigaciones viables y responder **CÓMO / POR QUÉ / PARA QUÉ**.
5. Solo tras ejecutar O1 y hacer síntesis crítica DR-05a, publicar O2 realmente justificadas en el mismo índice del HTML; O3 requiere ejecutar O2. Revisión visual DR-04 en la etapa apropiada y aprobación humana previa a audiovisual.

**Frente correspondiente:** DR-01/02/03 son investigaciones iniciales; DR-04 es visualización especializada diferida y DR-05 síntesis adversarial intermedia/final. Respetar `discovery_labs/shared/skills/question-forge/SKILL.md` y la metodología progresiva propuesta en PR #14.
