# DR-03 — Auditoría científica de mitos, antecedentes y diseño de hipótesis falsables sobre Bob Ross y The Joy of Painting

> **Recepción:** investigación compartida por el usuario el 19-11-2026, tercera de DR-01/02/03.  
> **Tipo:** archivo editorial estructurado del informe y sus anexos, **no transcripción literal íntegra del texto del chat**.  
> **Verificación:** hallazgos de prensa, cifras, links, estatus y calificaciones **provienen del estudio recibido**, sin nueva auditoría ni pruebas inferenciales en esta operación.  
> **Gobernanza:** archivo de entrada; NO modificar `QUESTIONS_MASTER.*`, NO presentar O2/O3 como preguntas activas del HTML, NO entrenar modelos, NO crear video.

## Propósito y caveats del estudio

El reporte se presenta como insumo para el único banco canónico de Bob Ross (403 episodios, 31 temporadas, 1983–1994). Su equipo no pudo abrir el repositorio DataCollectionMov ni el artículo web original de FiveThirtyEight; recurrió a copia del análisis Hickey, documentación de FiveThirtyEight/R, TidyTuesday, TwoInchBrush y trabajos citados. **No se ejecutaron modelos ni pruebas inferenciales sobre los CSV crudos.**

Promete siete productos: (1) 13 mitos/afirmaciones en `myths_claims.csv`, (2) 8 antecedentes en `antecedents.csv`, (3) explicaciones rivales, (4) 10 hipótesis H1–H10 con O1 y O2/O3 condicionales, (5) top 5, (6) contradicciones verificables, (7) necesidades de datos externos.

Los archivos **recibidos** se conservan aquí en una normalización estructurada:
- `DR-03_myths_claims.csv`: MC01–MC13.
- `DR-03_antecedents.csv`: ANT01–ANT08.
- `DR-03_rival_explanations.md`: R1–R5.
- `DR-03_questions_to_test.json`: H1–H10; su estado es PLAN_ONLY/CONDICIONAL, no inferencia ejecutada.

## 1. Afirmaciones y mitos documentados en el informe (por comprobar)

| ID | Afirmación | Respuesta reportada y reserva |
|---|---|---|
| MC01 | Árboles omnipresentes y «amigos» | Hickey reporta 91% ≥1 TREE y 85% ≥2; aproximadamente 9% sin árboles; confirmar denominador 381 |
| MC02 | Casi todas son montañas nevadas | ~39% con montaña, 66% de montañas nevadas; porcentajes según artículo Hickey, no reestimados |
| MC03 | Alaska inspiró los motivos y ritmo | Contexto biográfico documentado, no causalidad medible desde etiquetas |
| MC04 | Ross siempre pinta lo mismo | Grupos reconocibles pero rasgos raros y múltiples combinaciones; el número de clústeres depende de métrica |
| MC05 | Improvisaba sin planes | Tres versiones por obra según fuentes; robo de 13 referencias contado en foros, pendiente |
| MC06 | Paleta/repertorio inmóviles | Flourish describe desplazamiento Burnt Umber→Dark Sienna, sin contraste propio |
| MC07 | PBS era escaparate del negocio | Relación con Bob Ross Inc. y ventas citada, finanzas comerciales sin auditar |
| MC08 | Solo 3% pintaba junto a él | Atribución a Ross en LitHub, **no encuesta independiente** |
| MC09 | Invitados pintaban igual | Steve Ross/lagos y retrato de John Thamm muestran géneros distintos, con curación editorial como rival |
| MC10 | Ross inventó wet-on-wet y Liquid White | Técnica histórica / Bill Alexander anterior; distinguir marcas y procesos |
| MC11 | Duelo/linfoma determinaron obras tardías | Eventos históricos sí, **efecto pictórico no probado y diagnóstico disputado** |
| MC12 | Recepción posterior ASMR/Twitch | Múltiples trabajos; recepción no medida por CSV |
| MC13 | Nunca personas ni chimeneas | Reporte de 1–2 excepciones y denominadores contradictorios (0.26% vs 0.52%); no existe columna PERSON/CHIMNEY confirmada en CSV original |

**Precaución de fuente:** «Refutado» en una fila heredada significa conclusión *atribuida al informe*, no veredicto independiente. Un mito debe conservar quién lo afirmó, cuándo, fuente y popularidad comprobada; no llamar «popular» a una provocación sin evidencia.

## 2. Ocho antecedentes y brechas recibidas

| ID | Obra citada | Alcance / resultado reportado | Reservas |
|---|---|---|---|
| ANT01 | Walt Hickey (2014), FiveThirtyEight | Frecuencias condicionales y k-means k=10 sobre 403/381 y 67 tags | Un anotador, sin fechas/color, posible suma de clústeres 405 vs 403 |
| ANT02 | Graten, Hall & Hall (2015), ASIST | Visualización de temas, 403 episodios, 3,324 tags reportados | Contradicción 3,324 vs 3,224 / 3,221, póster sin replicación |
| ANT03 | Kwon et al. (2018), *Clustervision*, IEEE TVCG | Diversos algoritmos sobre ~400 pinturas; varias métricas internas | k preferido menor; sin datos de paletas |
| ANT04 | HookedOnData (2019) | Rasgos por cuadro, mitad de serie, PCA | Corte S1–15/S16–31 arbitrario, R blog |
| ANT05 | fivethirtyeightdata (2021) | Viñeta R de frecuencias, correlaciones y red S1 | Excluye invitados y tres incompletas, no población completa |
| ANT06 | Flourish/Wilber (2023) | Mapas de calor de 18 colores y medios en 403 episodios | Sin test de puntos de cambio, figura de pixeles de cuadro único |
| ANT07 | RollingStorms *Bob-Ross-Authenticator* | CNN de mosaicos para autenticación de pinturas | Sin revisión por pares, desequilibrio/clases y licencias |
| ANT08 | Howell & Howell (2022–23), JCMS | Recepción como comfort TV y escapismo | Cualitativo, no vincula audiencia a etiquetas/pinturas |

**Referencias:**
- Hickey: https://andyborne.com/math/StorageForFreebies/TinyLibrary/Art/bob-ross.pdf
- ASIST: https://www.researchgate.net/publication/275414108_Viewing_art_through_information_visualization_A_case_study_of_Bob_Ross's_The_Joy_of_Painting
- Kwon: https://www.researchgate.net/publication/319375523_Clustervision_Visual_Supervision_of_Unsupervised_Clustering
- HookedOnData: https://hookedondata.org/posts/2019-08-05_clustering-bob-ross-paintings/
- fivethirtyeightdata: https://fivethirtyeightdata.github.io/fivethirtyeightdata/articles/bob_ross.html
- Flourish: https://flourish.studio/blog/bob-ross-data-visualization/
- RollingStorms: https://github.com/rollingstorms/Bob-Ross-Authenticator
- Howell: https://muse.jhu.edu/article/899237/summary

## 3. Ocho contrastes recibidos

1. **Improvisación vs planificación:** tras una presentación televisiva espontánea habría preparación de tres versiones de obra.
2. **Primera vs última etapa:** cambios de música/edición/materiales/pigmentos, pero falta contraste formal y precisión de rodaje.
3. **Frecuencias marginales vs coocurrencia:** relaciones condicionales de playa/nube, ola/océano y árbol/montaña; cuidado con condicionales invertidas.
4. **Agregado vs autoría:** n=403 ≠ n=381; Steve e invitados pueden sesgar frecuencias.
5. **Invitados vs anfitrión:** géneros artísticos asignados por producción, no muestra aleatoria de autores.
6. **Etiquetas vs pintura física:** discrepancias sobre personas/chimeneas, tres incompletas, 3,224 vs 3,324, listas de pigmentos vs píxeles reales.
7. **K-means vs distancia binaria/mezclas:** dependerá de métrica, ontología y número k; no hay una única taxonomía validada.
8. **Eventos personales vs cuadros:** biografía y fechas de emisión no permiten atribución clínica o emocional de patrones.

## 4. Explicaciones rivales transversales

- **R1 producción/tiempo:** formato ~26 minutos útiles y posible grabación en bloques; explicar composición sin suponer intención psicológica.
- **R2 negocio:** adopción de insumos, kits, proveedores, marcas; necesita fechas mercantiles reales, no inventadas.
- **R3 error de medición:** codificación manual, criterios de prominencia, iluminación/VHS/resolución; comparar definiciones antes de llamar error.
- **R4 invitados curados editorialmente:** selección de géneros y artistas condiciona diferencias; estratificar por tema/temporada.
- **R5 física wet-on-wet y perspectiva:** composiciones pueden reflejar técnicas y geometría, no preferencias independientes.

Consultar `DR-03_rival_explanations.md` para controles sugeridos.

## 5. Diez hipótesis recibidas, todas planificadas

| ID | Tema | O1 / prueba de interés | Datos y bloqueos principales |
|---|---|---|---|
| H1 | Ruptura de color Burnt Umber vs Dark Sienna | Segmentar tasas de uso y `num_colors`; Fisher/permutaciones | Paletas externas, temporalidad de productos |
| H2 | Duelo/enfermedad y temporadas tardías | Diferencias descriptivas entre S10–25 y S26–31, NO inferencia clínica | Fecha de grabación, color real legal, cronología clínica disputada |
| H3 | Límite 26 min y estructuras vs naturaleza | Quasi-Poisson natural_element_count, Welch/permutación | Estructura y motivos del CSV |
| H4 | Firma anfitrión vs invitados | Jaccard/PERMANOVA, Fisher para LAKE | n=22, créditos de invitado, género y color |
| H5 | Concordancia etiquetado 2014 vs nuevas anotaciones | Kappa/McNemar y latentes | Imágenes autorizadas, libro de códigos; PERSON/CHIMNEY no deben inventarse |
| H6 | Robustez clústeres binarios + paletas | KMeans/PAM/Bernoulli, ARI/Silhouette/Mantel | Calidad de paleta y ontología, no imponer k=10 |
| H7 | Paleta declarada vs color en píxel | CIELAB, Spearman y modelos mixtos | Imágenes/licencias y calibración; `num_colors` ≠ diversidad visual |
| H8 | Inhibición de repetición intra-temporada | Markov y 10,000 permutaciones por temporada | Puede hacerse solo con etiquetas e IDs |
| H9 | Humanidad implícita: cabañas y nieve | OR exactas/logit para estructuras vs clima | Figuras humanas no observadas en esquema original; interpretación simbólica no identificada |
| H10 | Rasgos de episodio vs atención digital | Binomial negativa y devianza incremental | YouTube API, recreaciones y fecha de publicación, derechos/consentimiento |

**O2/O3:** solo diseños internos con trigger; no activar ni publicar preguntas de segundo orden hasta medir O1, cruzar DR-01/02/03 y realizar síntesis DR-05a. O3 requiere O2 medida y prueba rival. El JSON acompañado conserva esas dependencias.

## 6. Ranking publicado por el informe

**Puntuación de origen, sin validación nueva**: ocho dimensiones 1–5 (originalidad, valor científico, sorpresa honesta, reproducibilidad, disponibilidad de datos, falsabilidad, potencial visual, enseñanza 45 min), máximo 40.

| Puesto | Hipótesis | Puntuación reportada |
|---|---|---:|
| 1 | H5 — Nueva anotación vs etiquetas originales | 39 |
| 2 | H1 — Ruptura cromática Burnt Umber/Dark Sienna | 39 |
| 3 | H6 — Estabilidad y métrica de clustering | 38 |
| 4 | H7 — Paleta declarada vs píxeles CIELAB | 38 |
| 5 | H8 — Programación/inhibición secuencial | 38 |

**Advertencia del archivado:** puntuaciones «disponibilidad 5/5» de H5/H7 no equivalen a permiso para acceder/reutilizar 403 imágenes; no incorporar automáticamente ese ranking al roadmap. H8 necesita principalmente CSV base y su licencia de datos, mientras H5/H7 necesitan permisos concretos.

## 7. Dependencias externas destacadas

- **H2:** cronología de grabación y eventos biográficos de fuentes verificables; no inferir efecto del linfoma o duelo.
- **H4:** lista completa y consistente de créditos de los 22 invitados y contraste Steve/otros, imágenes en O3 solo con derechos.
- **H9:** transcripciones permitidas para O2 y nueva anotación visual para O3.
- **H10:** métricas externas de YouTube/TwоInchBrush, fecha de subida, controles de exposición, respeto a API/TOS; audio/comentarios solo bajo condiciones legales.
- **H5/H7:** el propio O1 depende de material visual protegido o con permisos no claros, a pesar de la clasificación optimista del estudio.
- **H1/H6:** dependen de esquemas de paleta y reglas de unión verificadas; no atribuir cambio de pigmento a decisiones comerciales sin evidencia.

## 8. Regla de incorporación

Este archivo conserva **material entrante** en una carpeta separada, sin reescribir las 14 investigaciones canónicas. Comparar H1–H10 con BR-01…BR-14 y los hallazgos recibidos de DR-01/02, validar IDs, duplicidades, evidencias y bloqueos; luego solo se propondrán cambios con trazabilidad y autorización. A la fecha de archivado **no hay entrenamiento ni validación científica de estas hipótesis**.
