# Plan científico · Bob Ross: la historia de una serie y sus paisajes

**Estado: PROPUESTA DE FASE 0.** No es aún informe científico validado ni guion del video.

## Norte de investigación

**Pregunta madre:** ¿Qué cambió, qué persistió y qué quedó fuera de lo que el mundo recuerda de Bob Ross durante los años de *The Joy of Painting*?

El dataset ofrece **403 episodios × 69 columnas, 67 etiquetas binarias, 31 temporadas**. La historia biográfica, la salud, la fecha real de grabación, los derechos de pinturas, su recepción y otros materiales requieren **fuentes adicionales verificadas**.

No empezar con "¿cuántos árboles?". Empezar por la historia y una hipótesis humana: ¿fue una obra que se transformó durante 11 años o una fórmula deliberadamente estable? La respuesta no está predeterminada.

## Lotes de trabajo con puertas

| Lote | Objetivo | Evidencia para continuar |
|---|---|---|
| 0 | Origen y derechos, 12 filas de muestra, metadatos | Fuente y hash; sample identificado como no representativo; ficha derechos |
| 1 | Deep Research histórico/biográfico/visual/literatura | Timeline con fuentes; producción ≠ emisión; ledger, contradicciones |
| 2 | Perfilado y evolución temporal | Bronze/Silver, tasas 31 temporadas, intervalos y n; QA; modelo nulo |
| 3 | Excepciones y preguntas de orden 2/3 | Outliers episodio/temporada/era; rare combos; refutación |
| 4 | Clustering e inspector visual de episodios | Métodos comparados; trazabilidad de obra/imagen; permiso o fallback |
| 5 | Selección editorial de tres investigaciones | Scores + estado de viabilidad por dato, narrativa humana y límites |
| 6 | Guía científica HTML fase 1 | Solo investigación ejecutada; revisión humana requerida |

Un "lote terminado" debe contener scripts, resultados, visualizaciones validadas y límites, no solo ideas.

## Hipótesis científicas rivales (no hallazgos)

**H-A Evolución:** la composición multivariante de motivos cambió gradualmente con temporadas.
- Rival: la composición fue estable, el aparente cambio se debe a invitados, rarezas o etiquetas.
- Test: evolución por motivo, comparación de agregación, cambio de punto con control de multiplicidad.

**H-B Salud:** los temas codificados cambiaron alrededor de un evento biográfico.
- Rival: no hay datos de producción suficientemente precisos o episodios posteriores comparables.
- Test: contrastar fecha de diagnóstico, filmación y emisión; si no hay solapamiento temporal identificable, **BLOQUEAR la inferencia causal**.

**H-C Outliers:** una temporada parece más atípica que la esperada.
- Rival: artefacto por buscar el máximo entre 31 temporadas o usar frecuencias de etiquetas raras.
- Test: permutaciones por tamaño y revisión de motivos raros; sensibilidad con invitados y 12/67 etiquetas.

**H-D Repetición:** las mismas combinaciones aparecen una y otra vez.
- Rival: los perfiles binarios ocultan diferencias visuales reales.
- Test: unicidad de perfiles y novedad cronológica; imágenes solo con derechos.

**H-E Segmentación:** las salas parecen naturales para un criterio y artificiales con otro.
- Rival: k=4 impuesto, dominancia de árboles y métrica seleccionada.
- Test: Jaccard vs Euclídea, exclusión de árboles, estabilidad, revisión de representantes.

## Variables y análisis

- RAW: EPISODE, TITLE, GUEST, 66 etiquetas restantes; fuente fijada, sin sustitución.
- SILVER: temporada, indicador de invitado, 12 familias OR; guardar también 67 etiquetas originales.
- GOLD: episodio, temporada, eras con definición explícita, proporción de motivos, rareza relativa, coocurrencia, asignaciones de cluster, incertidumbre.
- Universo: 403 episodios; subconjunto anfitrión 381; invitados 22. Comparar filtros con n visibles.
- Tiempo: extraer secuencia de EPISODE y, si se incorpora fecha de emisión, añadir nueva tabla con procedencia; **no fingir fecha de creación**.
- Baseline: prevalencia global, permutación estratificada, comparación descriptiva antes de ML.
- Pruebas adversariales: efectos de temporada, mezcla de invitados, redefinición de SNOWY_MOUNTAIN, feature leakage, rareza de categorías, multiplicidad.

## Preguntas y visualización

El archivo `QUESTION_GRAPH.md` ofrece 12 arcos con 24 preguntas de segundo orden y 12 de tercero (todos aún candidatos). El HTML futuro debe narrar **una historia de Bob Ross**: origen de la serie, formas de pintar, cambios de motivos, excepciones, contexto externo, contradicciones, límites y legado, sin convertirlo en un video.

Figuras: consulta `VISUAL_SPEC.md`. Ninguna ilustración de Bob Ross entra en repo o video hasta verificar permisos.

## Aprobación

0. Paquete revisado para iniciar Deep Research.
1. HTML científico `research_guide.html` con todas las pruebas, figura y aprobación explícita del usuario.
2. Solo entonces HTML de storytelling audiovisual; requiere su propia aprobación.
3. Solo entonces el video.

Rechazar lenguaje como «la enfermedad le hizo pintar más oscuro», «su estilo evolucionó porque...» o «su mejor temporada es...» hasta demostrar identificación y la métrica adecuada.
