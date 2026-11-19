# PROMPT EJECUTABLE — Fase 1 mejorada: guía científica HTML

## Único entregable
Crear/actualizar `discovery_labs/episodes/bob-ross/research_guide.html`, un **artefacto científico narrativo** de máxima calidad. Este HTML no es el video, ni el guion del video, ni un trailer. **Prohibido crear Fase 2/Fase 3 sin aprobación explícita.**

Trabaja exclusivamente en `discovery_labs/episodes/bob-ross/` y lee primero el paquete `entry_pack/` completo. Conserva todos los datos originales y pruebas. En caso de cambios sin guardar, no sobrescribirlos; auditar branch/PR antes.

## Orden de ejecución — no adelantarse

1. **Leer y verificar inputs:** `metadata.json`, `data_sample.csv`, `sources.json`, `QUESTION_BANK.md`, `question_graph.json`, `PLANNING.md`, `VISUAL_EVIDENCE.md`, `skills/research-question-architect/SKILL.md`, `DEEP_RESEARCH_PROMPTS.md`, CSV completo y scripts existentes.
2. **Ejecutar Deep Research por especialidades:** biografía y cronología; ciencia previa y nuevas fuentes; preguntas profundas con ramificaciones; derechos/visualizaciones; síntesis red-team. Si no hay acceso a búsqueda, poner BLOQUEADO y no inventar fuentes.
3. **Preparar ledger de afirmaciones y cronología:** hechos biográficos, fechas de emisión/filmación con confianza, resultados calculados, especulaciones; vincular IDs de fuente y archivos ejecutados.
4. **Preprocesamiento y enriquecer:** validar SHA; Bronze/Silver/Gold; examinar duplicados, nulos, etiquetas, grano; agregar por episodio, temporada, periodos verificados. Si se importan paletas/fechas, control de joins 1:1, cobertura y licencias.
5. **Preguntas:** conservar seis perspectivas A/B/C/D1/D2/E como rutas posibles, pero usar 12 árboles candidatos para seleccionar 2–4 investigaciones científicas protagonistas. Por cada una, orden 1 observado, segundo orden derivado de resultados (con triggers explícitos), tercero adversarial/explicación rival. Si un primer orden no muestra patrón, adaptar la pregunta en lugar de inventarlo.
6. **Ejecutar y auditar resultados:** métodos apropiados, no forzar ML; cambios temporales con placebo/cortes alternativos y exclusión de invitados; anomalías por episodio, temporada y bloque, incertidumbre; confusores y límites.
7. **Construir el HTML de lectura:** título histórico atractivo y comprobable; abrir con la vida de Bob Ross (hechos citados), su programa y el problema medible; introducir datos y sesgos; guiar por descubrimientos reales y sus pruebas. Modalidad narrada y técnica; índice, notas, figuras, métodos y fuente al lado de cada resultado.
8. **Visuales excepcionales:** timeline de vida vs patrones (sin causalidad automática), mapa de calor 31 temporadas, detector de anomalías multi-escala, comparador de paletas cuando verificado, cluster lab Jaccard/Euclídea con transiciones. En gráfico de clusters: pasar cursor/foco/clic sobre episodio debe mostrar ficha, título, motivos, temporada y **pintura real solo con derechos de uso verificados**; en caso contrario placeholder y enlace externo, sin copiar la obra. Mobile tap, teclado, screen-reader y fallback offline.
9. **Control editorial:** sin guion cinematográfico, Remotion, narración vocal, intro, vídeo ni MP4. El HTML es una guía de investigación, **no** una presentación audiovisual disfrazada.
10. **QA reproducible:** revisar cálculos, HTML real en Chromium escritorio/móvil, navegación teclado, gráfica con fuente, tooltip seguro, cargas/error, enlaces, permisos, coherencia de números, evidencia de render.
11. **Entregar únicamente Fase 1:** archivo real, datos/versiones, pruebas y screenshots, hallazgos + límites. Dejar `APPROVAL_STATUS=PENDING` y detenerse.

## Criterios específicos de calidad

- **La historia de Bob Ross no es adorno:** se documenta su trayectoria, sucesos, contexto histórico y vacíos, se explica de qué modo las fechas externas conectan —o no— con temporadas.
- **La salud es una hipótesis a investigar, no una conclusión:** si se dispone de fuente para fecha de diagnóstico, estudiar coincidencias descriptivas y robustez; no suponer que causó cambios, no inferir capacidad/estado desde cuadros. Si faltan fechas/grado de evidencia, NO ejecutar una comparación clínica.
- **Todas las preguntas principales son profundas:** no culminar en simples COUNT o yes/no; se muestra orden 1 → segundo orden condicionado → tercero que cuestiona mecanismo o proxy.
- **Creencias de alto nivel:** «¿repetía su fórmula?», «¿tenía un estilo invariable?» o «¿el personaje público coincide con los datos?», solo como hipótesis si su difusión cultural no está documentada.
- **Outliers a varias escalas:** episodio, temporada y periodo, con prueba leave-one-out y distinción de población/invitados.
- **Visualización narrativa potente:** cada gráfico agrega contexto, evidencia, interpretación y refutación. Ver `VISUAL_EVIDENCE.md`.
- **Derechos y fuentes:** no asumir que licencia de etiquetas autoriza pinturas/videos/audio. Llevar registro por activo, atribución y enlace.
- **Rigor técnico:** resultados reproducibles, sin leakage, tamaños muestrales y denominadores, métodos sensibles a pequeñas n, estado de cada conclusión.
- **Aprobación obligatoria:** no comenzar el storytelling audiovisual ni el video sin intervención expresa del autor.

## Resultado a mostrar al usuario
Proporcionar enlace al `research_guide.html`, resumen de 3–4 hallazgos realmente comprobados, problemas que impidieron investigar algo, impacto de fuentes externas, inventario de visualizaciones revisadas, batería de pruebas y estado de revisión. **Pedir aprobación de Fase 1.**
