# AI DISCOVERY LABS — BO​B ROSS · FASE 0 → FASE 1 (NO VIDEO)

**Rol:** equipo de historiador de medios, Senior Data Scientist, Data Engineer, investigador de cultura visual, estadístico adversarial, científico de visualización de datos y diseñador de experiencias científicas interactivas.

**Repo:** https://github.com/jcval94/DataCollectionMov

**Carpeta ÚNICA autorizada:** `discovery_labs/episodes/bob-ross/`. Trabaja sobre la rama más actual del episodio, preservando cambios locales y PRs concurrentes. No tocar `mvp-ds-course`, workflows globales ni otros proyectos.

## Resultado que quiero
**Un único artefacto de Fase 1:** `research_guide.html` (y su pipeline/evidencias locales) que narre la **historia de Bob Ross** y la investigación técnica **mediante gráficos memorables, hallazgos reales, preguntas de varios órdenes y análisis adversariales**.

NO quiero seis simples preguntas de consulta. El CSV es el punto de partida; debes investigar el contexto real de 1983–1994, la trayectoria artística, datos no incluidos, influencia de la producción y el riesgo de atribuir cambios a eventos personales sin diseño causal.

**Bloqueo de gobernanza:** NO crear ni actualizar guion audiovisual, storyboard de video, intro, voz, subtítulos, Remotion ni MP4. Eso es Fase 2/3 y requiere aprobación humana de la guía.

## 0. Aterrizaje y auditoría (obligatoria)
1. Detecta carpeta local, rama, PR #5 y cambios sin guardar. No hagas reset destructivo.
2. Revisa `entry_pack/README.md`, `metadata.json`, ambos CSV de muestra, `QUESTION_ARCS.md`, `question_graph.json`, `RESEARCH_PLAN.md`, `VISUAL_DESIGN.md`, y `skills/question-forge/SKILL.md`.
3. Ejecuta `run.py --check`, tests del episodio, verifica hash del original, licencias y fechas; distingue resultados previamente calculados de los tuyos.
4. Inspecciona la guía HTML preliminar si está disponible. **No la apruebes por su apariencia**.
5. Establece una matriz de errores/faltantes y dependencias.

## 1. Deep Research (cuatro ejes + síntesis)
Sigue `entry_pack/DEEP_RESEARCH_PROMPTS.md`:

- DR-01: biografía, historia de la serie, fechas, acontecimientos documentados.
- DR-02: arqueología del dataset, cronología grabación/emisión y metadatos externos de colores/pinturas.
- DR-03: mitos REALES, antecedentes y mecanismos alternativos.
- DR-04: imágenes, derechos, visualizaciones, explorador de clusters con hover/focus.
- DR-05: reconciliar hechos, cuestionar hipótesis, priorizar preguntas.

Cita URLs y fecha de acceso en un registro. Establece `VERIFIED`, `DISPUTED`, `PENDING` o `NOT_SUPPORTED`; **nunca marques como ejecutada una investigación que sólo fue sugerida**.

**Caso crítico:** explorar si aparece algún cambio pictórico tardío y qué evidencia contextual existe sobre la enfermedad de Bob Ross. No afirmes que la enfermedad lo causó. Verifica fecha del diagnóstico y orden de grabación de cada episodio antes de situar eventos sobre un gráfico. La temporada ordinal no es una fecha clínica. Puede ser imposible inferir el efecto: decirlo explícitamente.

## 2. Preguntas que atrapen (skill Question Forge)
Usa `entry_pack/skills/question-forge/SKILL.md` y **rehaz la selección editorial**. Lee los 12 arcos existentes como candidatos, no verdades.

Para cada historia principal:
- Una pregunta raíz O1 no reducible a un conteo plano.
- Una segunda pregunta O2 **gatillada por un resultado medido**, no inventada.
- Al menos una pregunta O3 que cuestione O2 por heterogeneidad, fuente externa, robustez o mecanismo.
- Métricas/estimandos, denominadores, baseline, filtros, métodos, pruebas adversariales.
- Ruta «hallazgo apoyado / refutado / inconcluso».
- Priorización editorial y plan de visualización.
- Preguntas sobre evolución, periodos históricos, outliers episodio/temporada/era, coocurrencias no triviales, procesos, selección de la muestra, mitos acreditados y modelos engañosos.

**Prohibición:** presentar `COUNT(TREE=0)` como la historia completa. Úsalo como una escena de evidencia dentro de una pregunta mayor.

## 3. Data Engineering y experimentación
Desde los 403 episodios originales, construye Bronze/Silver/Gold reproducible y versionado. Valida duplicados, ceros, tags correlacionados, filtros GUEST, temporadas, perfiles, joins con paleta y cronología, calidad externa y signos de sesgo.

Prueba cambios temporales, outliers multiescala, prevalencia condicional, coocurrencias contra esperado, sensibilidad de grupos y explicaciones rivales. Explica métodos, incertidumbre, tamaños de muestra y limitaciones. No fuerces modelos complejos.

Mantén gráficos y números derivados de salidas estructuradas, no del HTML redactado manualmente.

## 4. Visualización poderosa (Fase 1)
Implanta las visualizaciones justificadas de `VISUAL_DESIGN.md` como argumentos de datos:

- Heatmap por temporada y motivo (n visibles).
- Episodios atípicos, temporadas atípicas y periodos de la serie.
- Explorador de clusters **con tarjeta al hover/focus/tap** (ID, título, 12 motivos, cluster, método, representante y contexto).
- Pintura real en miniatura SOLO si su licencia/derechos y mapeo `season/episode` han sido verificados; de lo contrario mostrar tarjeta factual de motivos y enlace al sitio original. No inventar imagen ni capturar sin permiso.
- Comparación Jaccard vs Euclídea y un ejemplo de episodio que cambia de grupo.
- Historia cronológica con banda de eventos externos, distinguiendo niveles de confianza.
- Figura adversarial por cada hallazgo importante.

Inspecciona los gráficos realmente renderizados, en laptop y teléfono. Accesibilidad keyboard-only, contraste, texto alternativo y salidas en SVG/PNG.

## 5. Documento guía científico
La guía debe sentirse como **un ensayo ilustrado riguroso sobre la vida televisiva de Bob Ross**, no como un reporte corporativo ni una colección de widgets.

Narración sugerida, adaptable a resultados:
1. Quién era Bob Ross y por qué importa.
2. 403 episodios y qué quedó fuera del archivo.
3. La iconografía que recordamos y su diversidad real.
4. Cómo evolucionó el repertorio de motivos.
5. Las excepciones que reescriben nuestra primera impresión.
6. Clusters, métricas y diferencias entre modelos.
7. Eventos biográficos: coincidencias verificables y límites de la atribución.
8. Qué hace falta para investigar más allá del CSV.
9. Métodos y reproducibilidad.
10. Auditoría y puerta de aprobación.

Incluye **modo lector** (ensayo narrativo) y **modo técnico** (fórmulas, tablas, decisiones de limpieza, tests y código), accesible y responsive, sin dependencias de pago. Mantén datos originales y resultados versionados.

## 6. Criterios de aceptación
- 403 filas y hash originales comprobados.
- Afirmaciones biográficas citadas y temporalidad separada.
- Al menos tres arcos O1→O2→O3 investigados cuando los datos lo permitan o declarados bloqueados con motivo.
- Tests de datos y cálculos; QA real de figuras, HTML, teclado/móvil y elementos hover/focus.
- Ninguna pintura mostrada ilegalmente; sin datos/fotos inventados.
- Rigor: las hipótesis inconclusas no se venden como insights.
- Un archivo HTML autosuficiente con tabla de contenido, hallazgos, fuentes, método y QA.
- Estado `PENDIENTE_DE_APROBACION`.

## 7. Entrega
Documenta archivos tocados (solo carpeta del episodio), commits o PR, comandos ejecutados, pruebas/errores, decisiones editoriales, fuentes, cinco mejores hallazgos SOLO si están calculados, preguntas de orden superior activadas y pendientes por datos externos.

Proporciona la ruta navegable de `research_guide.html` y **DETENTE**. La siguiente etapa no existe hasta que yo apruebe explícitamente esta versión del documento científico.

**Empieza ya por el paquete de entrada y la investigación documental, luego ejecuta los análisis y actualiza exclusivamente el primer HTML.**
