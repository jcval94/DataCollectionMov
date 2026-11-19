# DR-02 — Auditoría arqueológica, integración multisource y potencial científico del dataset de Bob Ross

> **Recepción:** investigación aportada por el usuario el 19-11-2026.  
> **Tipo:** archivo estructurado de metodología, fuentes, riesgos, hallazgos publicados y propuestas recibidas; **no es una reproducción literal íntegra del texto enviado en la conversación**.  
> **Verificación:** los estados AVAILABLE/PARTIAL/PENDING/BLOCKED corresponden al informe recibido, **no a una auditoría independiente realizada al archivar**.  
> **Uso:** investigación entrante, separada de los contratos canónicos. No hay entrenamientos ni nuevos resultados inferenciales.

## 0. Resumen de tesis y alertas metodológicas

El informe ubica el origen de `elements-by-episode.csv` en FiveThirtyEight/Walt Hickey (artículo de 14 abril 2014), derivado de inspección manual de fotografías comerciales de Bob Ross Inc., **no de mediciones continuas sobre video, imágenes físicas o fotogramas originales**. La tabla fuente contiene 403 episodios y 69 columnas (EPISODE, TITLE y 67 etiquetas binarias), según documentación.

Se proponen cuatro limitaciones que cualquier análisis debe reconocer:

1. **Desalineación potencial de versión pictórica:** foto de tienda, cuadro “tv”, lienzo “Kowalski” y lienzo “book” pueden no coincidir plenamente; comparar imágenes de otra versión no garantiza que las etiquetas originales midan lo mismo.
2. **Diferencias de autoría:** 381 episodios atribuidos al anfitrión y 22 a invitados; el análisis del estilo de Ross debe separar o controlar GUEST.
3. **Ausencia de cronología de grabación:** temporadas y fechas de emisión no son fechas de creación pictórica.
4. **Etiquetado binario incompleto:** no mide cantidad de árboles, área, tono, textura, jerarquía espacial ni ausencia deliberada. Ciertos atributos son de encuadre, no paisaje, y otros representan autoría.

El equipo DR-02 no pudo inspeccionar remotamente la copia del repositorio DataCollectionMov y dejó SHA local como pendiente. Esta afirmación corresponde **al entorno del informe**, no al acceso que pueda tener otro agente al GitHub conectado. Archivo/hash comunicados por el proyecto: 403×69, 66,315 bytes, SHA-256 `42045c8b8aaa8296095d6b294927fb9d0f73a57259f59b560c375844c0fe01cf`. El archivado no recalcula ese hash.

**Discrepancia importante para contrastar:** artículo de Hickey cita **3,224 etiquetas positivas**; proporciones de análisis secundarios sugerirían **3,221**; otro documento académico citado por DR-03 menciona **3,324**. No decidir por autoridad textual: calcular suma exacta sobre la matriz del snapshot versionado y reconstruir qué filas/etiquetas incluye cada autor.

## 1. Dataset y sesgos documentados

- Codificación humana de fotos de catálogo BRI hecha por una persona; sin evaluación inter-anotador publicada, según el informe.
- Variables binarias sobre paisaje (TREE/TREES, CLOUDS/CUMULUS/CIRRUS, SNOWY_MOUNTAIN...), clima, estructuras, tipos de marcos y artistas invitados. Ninguna densidad cromática real o rasgo físico continuo.
- Ejemplos de dependencias por construcción: CLOUDS / CIRRUS / CUMULUS; FRAMED y subtipos de marco, etiquetas de montaña/nieve. **No interpretar coocurrencia jerárquica como mecanismo artístico descubierto.**
- Ceros de ausencia no distinguen «no visible», «no prominente», «no codificado» o «no buscado» salvo definición explícita del libro de códigos.
- Duplicado exacto de título `LAKESIDE CABIN`; la viñeta R renombraría S08E02 `LAKESIDE CABIN 2`. Usar `EPISODE` como llave; jamás el título.
- Tres filas excluidas en la viñeta R derivada como cuadros incompletos: `PURPLE MOUNTAIN RANGE`, `COUNTRY CHARM`, `PEACEFUL REFLECTIONS`. **No excluirlas silenciosamente del CSV original**; conservar bandera de análisis y rastro del filtro.
- Autoría reportada en la tabla: n=381 anfitrión, n=22 invitados; listas externas mencionan 20 apariciones o nombres diferentes. Conciliar por código de episodio y créditos, no por nombres parcialmente observados.
- El supuesto de que un valor 0 representa ausencia pictórica real debe probarse contra libro de codificación y calidad de las imágenes.

## 2. Cronología y riesgo de fuga

**Cuatro fechas distintas:** (1) creación/grabación de episodio, (2) primer estreno PBS, (3) repetición televisiva, (4) subida digital; las tres últimas no prueban fecha de ejecución del lienzo.

| Intervalo reportado | Temporadas | Advertencia |
|---|---|---|
| Ene 1983–nov 1984 | T1–T4 | Pausas intertemporada, 2 ciclos por año |
| Ene 1985–nov 1990 | T5–T21 | 2–3 ciclos por año y cadencia irregular |
| Ene 1991–mar 1992 | T22–T24 | Pausas prolongadas |
| Ago 1992–may 1994 | T25–T31 | Ciclos acelerados; no inferir mayor productividad pictórica |
| 2024–2026 | T32–T34, continuación | **Fuera de la población original 403×69** |

El informe afirma que T25–T31 son 91/403 = 22.6% de episodios y 630 días, ~15.2% de la ventana cronológica completa (~4,144 días). Estos cálculos **deben reconfirmarse** con definiciones de intervalo y fechas de primera emisión. El usuario aportó la alerta de que el índice ordinal de temporada comprime/distribuye la evolución temporal de forma irregular. Sin fechas de filmación, el uso de primera emisión introduce otros sesgos y no permite datar cambios clínicos.

Riesgo de leakage: ajuste de PCA, estandarización, imputaciones, centroides, variables de color y selección de features usando futuras temporadas antes de cortes OOS. Usar rolling-origin si la tarea justifica evaluación temporal; no introducir leak en estadísticas descriptivas ni confundir criterios de validación predictiva con causalidad.

## 3. Inventario de fuentes complementarias recibidas

**Estados citados son evaluaciones del DR-02; verificar licencias y disponibilidad antes de descarga, uso o publicación.**

| Fuente y URL | Unidad y llaves | Campos/valor potencial | Licencia y acceso reportado | Reserva |
|---|---|---|---|---|
| FiveThirtyEight https://github.com/fivethirtyeight/data | episodio `SxxEyy` | 67 etiquetas binarias, TITLE | CC BY 4.0 para datos, MIT para código (según reporte) | Obtener snapshot, validar total de tags |
| jwilber/Bob_Ross_Paintings https://github.com/jwilber/Bob_Ross_Paintings | `(season, episode)` | colores, colores hex, `num_colors`, tags, links | CSV PARTIAL, imágenes BLOCKED; sin licencia explícita afirmada | CSV ≠ permiso para imágenes; fuente TwoInchBrush |
| Wikipedia https://en.wikipedia.org/wiki/List_of_The_Joy_of_Painting_episodes | temporada/episodio | fechas de emisión, reparto, sedes por época | CC BY-SA 4.0, AVAILABLE en bloques | Tabla completa por episodio aún no confirmada |
| frankiethull/BobRossColors https://github.com/frankiethull/BobRossColors | pintura/episodio a revisar | paletas 403; códigos/llaves por verificar | MIT según informe; PARTIAL esquema | Mapeo episodeID no auditado |
| fivethirtyeightdata https://fivethirtyeightdata.github.io/fivethirtyeightdata/articles/bob_ross.html | `episode` | R dataframe derivado 403×71, `guest`, filtros | Datos CC BY 4.0 | No confundir derivación con original |
| OpenBrush Landscapes https://huggingface.co/datasets/jaddai/openbrush-landscapes | obra externa | color/comparación externa | CC0 según informe | Corpus de otro dominio; verificar procedencia |
| WikiArtVectors https://www.mdpi.com/1099-4300/24/9/1175 | artista/obra/década | embeddings/color, baseline | licencia dataset no verificada | Distribución no comparable sin control |
| TwoInchBrush https://twoinchbrush.com/ | pintura/episodio | color/material/galería | propietario, scraping BLOCKED | No extraer imágenes/scrapear en masa |
| TheTVDB https://thetvdb.com/series/the-joy-of-painting/allseasons/official | temporada/episodio | fechas y créditos | API reglada, PARTIAL/BLOCKED | Respetar TOS, no asumir permiso |
| *The Joy of Parsing* https://medium.com/fathominfo/the-joy-of-parsing-4addce08969a | posible transcripción/episodio | lenguaje/texto | acceso corpus PENDING | No asumir CSV descargable |
| Ball State PBS https://ballstatepbs.org/bobs-happy-home/ | sede, periodo | hechos de producción macro | AVAILABLE para sedes | No brinda coordenadas por cuadro |

**Uso legal:** un CSV con licencia abierta no habilita descarga ni redistribución de pinturas, videos o subtítulos. Verificar requisitos específicos por activo y permitir análisis sin material visual protegido.

## 4. Llaves, cardinalidad y capas Bronze/Silver/Gold

**Llave canónica:** `(season, episode)` derivada de `EPISODE = SxxEyy`. Garantizar unicidad y no multiplicación de filas. Los títulos se conservan como datos, no como llave.

**Tabla de uniones esperadas:**
- fivethirtyeight ↔ variante R: ~403/403 1:1, con variantes de títulos y filtrado documentado.
- fivethirtyeight ↔ jwilber CSV: 1:1 por episodio; explotar colores como tabla 1:N; cobertura debe medirse, no asumir 403.
- fivethirtyeight ↔ BobRossColors: esquema exacto de joins pendiente; 403 paletas reportadas no implica llave correcta.
- fivethirtyeight ↔ Wikipedia: temporada/episodio de emisión (1:1), episodio→contexto temporada N:1; filtrar T32–34.
- Invitados: conciliar 22 de Hickey con 20 reportados en foro y cobertura parcial de Wikipedia. Mantener discrepancias.
- Paisajes externos: **sin llave directa**, solo comparación de distribuciones y sesgos de dominio.

**Bronze inmutable:** `raw_elements_by_episode`, `raw_jwilber_paintings_csv`, `raw_bobrosscolors`, `raw_wikipedia_episodes_html` (cuando licencias lo permitan) + manifiesto hash/licencia/fecha. **Excluir físicamente** pinturas protegidas.

**Silver reconciliado:** `dim_episode`, `dim_season_context`, `bridge_episode_tag`, `bridge_episode_color`, `dim_author_reconciliation`, `is_duplicate_title`, `is_vignette_incomplete`, `air_date_precision` (fecha exacta vs aproximación), ontología de 67 columnas, origen y criterio de cada transformación.

**Gold analítico:** `mart_bob_ross_clean`, `mart_chronology_descriptive` (evitar etiqueta «causal» salvo identificación), `mart_palette_perceptual_features` donde proceda, `mart_motif_topology`, `mart_external_landscape_baseline`. Separar n=381 del conjunto n=403 y presentar calidad de fuentes/joins.

## 5. Diez oportunidades científicas recibidas (diseños, no resultados)

| ID | CÓMO | POR QUÉ | PARA QUÉ | Condiciones y competidores |
|---|---|---|---|---|
| 01. Tiempo calendario vs temporada | Reindexar motivos/paletas por emisión y evaluar cambio segmentado | Ritmo irregular de temporadas puede distorsionar | Separar cronología de emisión de deriva visual observada | No fechas de rodaje; OOS temporal |
| 02. Regímenes de producción y patrocinios | Comparar T1 WNVC, WIPB casa y WIPB campus + periodos de marcas | Método/insumos/estudio pueden covariar | Evitar atribución a biografía sin control | Precisión del traslado y patrocinio |
| 03. Gramática y anomalías de composición | PMI/redes sobre motivo natural vs arquitectura, baja frecuencia | Combinaciones marginales ocultan relaciones raras | Crear índice de outliers y robustez | Dependencias jerárquicas y rareza espuria |
| 04. Complejidad temática vs economía de paleta | Cruzar conteos/entropía de motivos y `num_colors` | Paleta restringida quizá produzca escenas ricas | Evaluar eficiencia expresiva sin efectos causales | Validez del campo `num_colors` |
| 05. Ceros estructurales | Probar ausencia de figuras/chimeneas con modelos de cero/permutaciones | Puede haber reglas narrativas explícitas | Enseñar sesgo de medición y restricciones latentes | No hay columna de chimenea/persona en original confirmado |
| 06. Color declarado vs semántica | `colors_hex`→CIELAB y predictibilidad de WINTER/BEACH/FOG | Lista de materiales difiere del aspecto final | Frontera de interpretabilidad de paletas | No usar píxeles sin derechos |
| 07. Clustering por ontología/distancia | Comparar KMeans, PAM-Jaccard, bootstrap, ARI, silhouette | Clústeres pueden ser artefactos de métrica | Buenas prácticas para datos binarios | No imponer k=4 o k=10 |
| 08. Autoría invitados vs Bob | Control de temporada/género, probabilidades condicionales | Invitados no son muestra aleatoria | Medir sensibilidad de estadísticas agregadas | n=22, controles y coincidencias |
| 09. Forense de fuentes | Reconciliar 22 vs 20 invitados, 3224 vs 3221 vs 3324 tags, 3 incompletas y ontologías | Errores heredados cambian denominadores | Master confiable para el laboratorio | Necesita acceso a snapshots |
| 10. Bob Ross frente a paisajes históricos | Comparar paletas declaradas contra OpenBrush/WikiArt de uso permitido | Técnica televisiva vs otra tradición | Establecer una comparación cultural cautelosa | Sesgos grandes y licencia de corpus |

**Advertencias específicas:** la oportunidad 05 utiliza ejemplos de chimeneas/personas **no necesariamente representadas como columnas originales**, por lo que no se debe afirmar detectabilidad automática de normas usando una variable inexistente. La oportunidad 06 puede medir selección de pigmentos, **no luminancia real ni área cubierta por pigmento**. La oportunidad 10 es de comparación externa, no identidad de estilos sin imagen.

## 6. Cinco enriquecimientos priorizados por el informe

1. **Cronología y sedes/patrocinios**: Wikipedia y archivos institucionales, costo bajo, validar fechas.
2. **Paletas, códigos hex y medios**: BobRossColors MIT / jwilber CSV; no ingerir imágenes protegidas.
3. **Autoría de invitados**: tabla episodio a episodio y resolver diferencias de 20 vs 22.
4. **Ontología de indicadores**: separar paisaje, marco, técnica, autoría y dependencias entre etiquetas.
5. **Corpus histórico externo**: OpenBrush/WikiArt sólo con licencia comprobada y control de sesgo.

## 7. Riesgos generales

- **Fuga temporal:** PCA, normalizadores, selección de features, centroides o hiperparámetros entrenados con futuras temporadas antes de evaluación histórica.
- **Reloj equivocado:** emisión y creación no son equivalentes, especialmente temporadas grabadas en bloque.
- **Cambio de versiones:** catálogo comercial, video y libro pueden representar variantes del mismo cuadro.
- **Interpretación condicional:** P(A | B) != P(B | A); denominadores del anfitrión vs invitados no intercambiables.
- **Ontología:** subtipos de nubes/marcos/nieve activan relaciones por construcción y pueden inflar clustering/coocurrencia.
- **Derechos:** acceso web no supone autorización para scraping, redistribución de imágenes o entrenamiento visual.

## 8. Plan reproducible de validación propuesto

1. Calcular **SHA-256** en archivo exacto del repositorio y comparar 403×69 con snapshot original; calcular suma exacta de 67 etiquetas positivas para resolver **3,224 vs 3,221 vs 3,324**.
2. Afirmar clave EPISODE única S01E01–S31E13, TITLE no nulo, 67 indicadores estrictamente 0/1, duplicado de título y banderas de incompleto; documentar diferencias entre muestras CSV y paquete R.
3. Probar reglas de consistencia jerárquica: CLOUDS/CIRRUS/CUMULUS; FRAMED/subtipos; reportar excepciones sin inventar reparación semántica.
4. Validar joins con cobertura real y cardinalidad por fuente; separar Bob Ross (381) e invitados (22); resolver autoría y tres registros filtrados en la viñeta R.
5. En experimentos temporales usar rolling-origin y transformations sólo sobre pasado. Para coocurrencias plantear permutaciones con preservación de marginales por fila y columna cuando sea matemáticamente viable y definir unidad de bloqueo apropiada.

## 9. Puertas antes de integración

Este informe no implica que sus referencias, licencias, esquemas de archivos externos ni cálculos estén verificados. Antes de edición de preguntas canónicas, validar red y metadatos fuente, resolver sesgos y licencia; **no modificar modelos, HTML ni fuentes hasta autorización de la fase correspondiente**. Se archiva como DR-02 recibida.
