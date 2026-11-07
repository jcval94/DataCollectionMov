# De una fuente curiosa a un descubrimiento verificable

El objetivo de este catálogo es encontrar preguntas que no se nos habrían ocurrido y responderlas con evidencia. La IA ayuda a buscar, leer, clasificar, conectar y proponer explicaciones; los registros y documentos permiten comprobarlas.

Las preguntas siguientes son **hipótesis abiertas**, no hallazgos ya demostrados. El [piloto de Bob Ross](../examples/bob_ross_discovery/README.md) es una excepción explícita: incluye cálculos ejecutados y verificaciones. Las [pruebas de acceso](../source_tests/README.md) indican qué material se recuperó realmente.

La [matriz de exploración por fuente](exploration/README.md) amplía esta guía con **234 preguntas**, skills, MCP/herramientas, arneses y controles concretos para las 78 fuentes. Es un plan de trabajo; las respuestas y evaluaciones de método siguen pendientes.

## Mapa de temas y preguntas

| Tema pedido | Fuentes del catálogo | Qué podríamos descubrir | Papel de la IA y comprobación necesaria |
| --- | --- | --- | --- |
| Restaurantes | [Inspecciones NYC](CATALOGO_DATASETS_REALES.md#nyc-restaurantes), [OSM](CATALOGO_DATASETS_REALES.md#osm-mapas-restaurantes), [DENUE](CATALOGO_DATASETS_REALES.md#inegi-denue) | Infracciones que reaparecen, oferta por barrio y diferencias entre presencia real y cartografía incompleta. | Agrupar descripciones; distinguir una inspección de cada infracción y contrastar con otra fuente. |
| Aviones | [OpenFlights](CATALOGO_DATASETS_REALES.md#openflights-red-aerea), [BTS](CATALOGO_DATASETS_REALES.md#bts-puntualidad-vuelos) | Aeropuertos que conectan comunidades y franjas del día donde se acumulan demoras. | Explicar grafos y segmentos comparables; rutas históricas no equivalen a vuelos vigentes. |
| Apps | [Catálogo Apple](CATALOGO_DATASETS_REALES.md#apple-apps), [reseñas](CATALOGO_DATASETS_REALES.md#apple-resenas-apps) | Promesas de funciones que no coinciden con los problemas mencionados por usuarios. | Etiquetar quejas, validar una muestra humana y separar versión, país y selección de reseñas. |
| Viajes | [Inside Airbnb CDMX](CATALOGO_DATASETS_REALES.md#insideairbnb-cdmx), OpenFlights y [EOD](CATALOGO_DATASETS_REALES.md#inegi-eod-zmvm-2017) | Concentración de oferta turística y contraste entre moverse por turismo o por necesidad cotidiana. | Clasificar anuncios; no confundir disponibilidad con ocupación ni unir personas de fuentes distintas. |
| Napoleón | [Napoleonica](CATALOGO_DATASETS_REALES.md#napoleonica-cartas), [Gallica](CATALOGO_DATASETS_REALES.md#gallica-napoleon) | Diferencias en temas y vocabulario según destinatario, lugar y etapa. | Extraer entidades y citas; controlar género documental, traducción y edición. |
| Diarios personales | [Samuel Pepys](CATALOGO_DATASETS_REALES.md#pepys-diarios) | Ritmos cotidianos, relaciones, comidas y preocupaciones que cambian por estación o contexto. | Extraer entradas fechadas; separar voz del diarista de notas editoriales. |
| Diarios y prensa | [Periódicos LOC](CATALOGO_DATASETS_REALES.md#loc-prensa-historica), [GDELT](CATALOGO_DATASETS_REALES.md#gdelt-noticias) | Cómo cambia el lenguaje usado para describir una enfermedad, tecnología o protesta. | Buscar términos y contexto; medir cobertura de medios y errores OCR. |
| Literatura | [Quijote](CATALOGO_DATASETS_REALES.md#gutenberg-quijote), Pepys y [DraCor](CATALOGO_DATASETS_REALES.md#dracor-teatro) | Personajes que hablan mucho frente a personajes que conectan grupos o hacen avanzar conflictos. | Resolver personajes y referencias; contrastar la red con lectura de pasajes. |
| Conciertos | [MusicBrainz](CATALOGO_DATASETS_REALES.md#musicbrainz-conciertos), [setlist.fm](CATALOGO_DATASETS_REALES.md#setlist-conciertos) | Canciones de apertura/cierre, sorpresas y diferencias entre giras. | Homologar canciones y versiones; no inferir asistencia o gusto nacional a partir de cobertura desigual. |
| Mapas | [Mapas históricos LOC](CATALOGO_DATASETS_REALES.md#loc-mapas-historicos), OSM y [Marco Geoestadístico](CATALOGO_DATASETS_REALES.md#inegi-marco-geoestadistico) | Caminos, topónimos o cursos de agua que desaparecieron o cambiaron. | OCR y georreferenciación con puntos de control; separar deformación del mapa de cambio real. |
| Exámenes | [GSM8K](CATALOGO_DATASETS_REALES.md#gsm8k-examenes), [guías CCH](CATALOGO_DATASETS_REALES.md#unam-guias-examenes) | Tipos de problema donde una IA falla aunque el resultado parezca convincente. | Clasificar operaciones; evaluar con respuestas verificadas y evitar contaminación del benchmark. |
| UNAM | [Colecciones](CATALOGO_DATASETS_REALES.md#unam-colecciones), [Agenda Estadística](CATALOGO_DATASETS_REALES.md#unam-agenda-estadistica), guías CCH | Historia de colecta científica y diferencias de oferta o crecimiento por entidad académica donde existan cuadros comparables. | Extraer metadatos/cuadros; no inventar desagregación por plantel ni datos individuales. |
| Venta de inmuebles | [Transacciones Connecticut](CATALOGO_DATASETS_REALES.md#ct-ventas-inmuebles) | Operaciones cuyo precio parece anómalo y se explica por transferencias familiares, parciales o por clasificación. | Explicar grupos comparables; distinguir avalúo fiscal, precio de cierre y anuncio. Es un caso de EE. UU., no del mercado mexicano. |
| Baile | [AIST++](CATALOGO_DATASETS_REALES.md#aist-dance), [CMU MoCap](CATALOGO_DATASETS_REALES.md#cmu-movimiento-baile) | Movimientos que siguen un ritmo parecido pero usan patrones corporales distintos. | Comparar series temporales/poses; validar esqueleto, FPS y alineación musical. |
| Pintura clásica y arte | [Met](CATALOGO_DATASETS_REALES.md#met-arte), [Art Institute](CATALOGO_DATASETS_REALES.md#artic-pintura) | Motivos, materiales y paletas que cambian según periodo, artista y colección. | Comparación de imagen y texto; controlar reproducción, medio y sesgos del museo. |
| Teatro | [DraCor](CATALOGO_DATASETS_REALES.md#dracor-teatro) | Personajes secundarios que funcionan como puentes entre escenas o grupos. | Redes de copresencia e intervenciones; copresencia no siempre significa conversación. |
| Retail | [Online Retail UCI](CATALOGO_DATASETS_REALES.md#uci-retail), [Open Food Facts](CATALOGO_DATASETS_REALES.md#openfoodfacts-alimentos) | Productos que cambian de posición al descontar devoluciones, o patrones de ingredientes y etiquetado. | Agrupar descripciones; contrastar facturación bruta/neta y revisar unidades. Sin costos no hay beneficio calculable. |
| Medicina | [openFDA](CATALOGO_DATASETS_REALES.md#openfda-etiquetas), [CLUES](CATALOGO_DATASETS_REALES.md#salud-clues) | Diferencias de lenguaje entre etiquetas y de oferta territorial de servicios. | Extraer conceptos con citas; no convertir conteos de etiquetas o establecimientos en riesgo clínico o calidad de atención. |
| Literatura médica antigua | [Wellcome](CATALOGO_DATASETS_REALES.md#wellcome-medicina-antigua), Gallica y Pepys como contraste de género | Qué querían decir los textos al hablar del sueño, la vigilia, la higiene o una enfermedad. | OCR, lectura contextual y comparación entre autores; una receta médica no prueba que la población la practicara. |
| Bob Ross | [Motivos codificados](CATALOGO_DATASETS_REALES.md#bob-ross-elementos), [paletas e imágenes](CATALOGO_DATASETS_REALES.md#bob-ross-paletas) | Qué elementos coaparecen y si las paletas declaradas concuerdan con las imágenes. | Asociaciones con frecuencias base; revisión visual de episodios y derechos de las imágenes. |

## Caso de investigación: ¿era habitual despertarse a mitad de la noche?

La idea es fértil para investigar, pero la pregunta necesita lugar, época y población. Ekirch propuso una interpretación de sueño segmentado apoyada en testimonios históricos. Una revisión de Boyce cuestiona que todas las menciones a primer o segundo sueño indiquen dos bloques separados por una vigilia larga; Ekirch respondió defendiendo su lectura. No es correcto convertir ese debate en la conclusión universal de que todas las personas dormían igual antes de la industrialización.

Fuentes para contrastar el argumento:

- [Ekirch, 2001, *Sleep We Have Lost*](https://doi.org/10.1086/ahr/106.2.343): investigación original; el acceso al texto editorial puede ser limitado.
- [Boyce, *Have we lost sleep?*](https://pmc.ncbi.nlm.nih.gov/articles/PMC10404514/): investigación crítica sobre las interpretaciones y ambigüedades de los textos.
- [Ekirch, *Reflections on “Have we lost sleep?”*](https://pmc.ncbi.nlm.nih.gov/articles/PMC11655156/): respuesta del autor.

Una ruta reproducible:

1. Delimitar siglos, regiones y lenguas. Empezar por libros o diarios digitalizados con edición identificada y acceso permitido.
2. Recuperar pasajes sobre primer sueño, segundo sueño, vigilia, despertares y expresiones equivalentes. Guardar obra, autor, fecha, página, texto y URL/ARK.
3. La IA propone una etiqueta: práctica cotidiana explícita, consejo médico, enfermedad, metáfora, narración ficticia o caso ambiguo. Conservar el pasaje que permite comprobarla.
4. Una persona revisa una muestra de cada categoría y los desacuerdos. OCR incierto se coteja con la imagen de la página.
5. Contar autores y obras además de menciones: diez ediciones de una misma cita no son diez testimonios independientes. Añadir contraejemplos y textos de control.
6. Redactar sólo lo que el conjunto respalda, por ejemplo: «en este corpus y periodo aparecen testimonios explícitos de vigilia entre dos periodos de sueño». Evaluar por separado si puede generalizarse.

La prueba de Wellcome recuperó una ficha de *Sleep and dreams*, publicada en Londres en **1857**. Eso demuestra que encontramos un candidato histórico; **no** que hayamos leído todo el libro, recuperado su OCR completo o comprobado allí la hipótesis. La página, el contenido y sus derechos siguen siendo el siguiente paso de investigación.

Este caso es historia de prácticas e interpretaciones, no una recomendación de cambiar horarios de sueño.

## Qué hacer primero

| Caso | Por qué empezar aquí | Primer resultado comprobable |
| --- | --- | --- |
| Bob Ross | CSV pequeño y definiciones explícitas. | [Piloto ejecutado](../examples/bob_ross_discovery/README.md): conteos, frecuencias y sensibilidad excluyendo invitados. |
| Retail | Registros transaccionales con una trampa de negocio concreta. | Ranking bruto y neto tras separar cancelaciones; no calcular beneficio sin costos. |
| Apps | Metadatos y textos cortos para clasificación asistida. | Tabla de problemas recurrentes con citas breves, versión y revisión humana. |
| Teatro | Texto más estructura para contrastar dos lecturas de una obra. | Personajes por intervenciones y por centralidad, explicando cómo se construyó la red. |
| Medicina histórica y diarios | Potencial de sorpresa alto, mayor esfuerzo de contexto. | Corpus de pasajes clasificados, con contraejemplos y procedencia; conclusión delimitada. |

## Ficha mínima de un descubrimiento

Guardar: pregunta, alcance, fuente/edición, unidad de análisis, registros incluidos y excluidos, transformación, evidencia exacta, resultado, explicaciones alternativas y estado de validación. Usar tres estados visibles: **hipótesis**, **hallazgo descriptivo medido** e **interpretación todavía por contrastar**.

Para trabajar con un agente:

> Explora esta pregunta usando únicamente las fuentes indicadas. Propón explicaciones alternativas, extrae evidencia con identificadores verificables y calcula con un programa los conteos que uses. Separa hipótesis de resultados. Busca contraejemplos y no generalices fuera del corpus ni conviertas correlaciones en causas. Si falta acceso al contenido, registra la limitación y no lo sustituyas con memoria o citas inventadas.

El catálogo contiene acceso y posibilidades. El informe de pruebas demuestra qué se pudo recuperar. Una conclusión sobre el mundo requiere además validar el análisis.

## Deportes y juegos

La ampliación añade ajedrez de grandes maestros y archivos generales, fútbol soccer, Scrabble, básquetbol, Fórmula 1 y Dota 2: seis fuentes y 18 preguntas. Ver [fichas y controles específicos](CATALOGO_DATASETS_REALES.md#deportes-y-juegos) y [README de tests con registros reales](../source_tests/by_topic/deportes-y-juegos/README.md). El interés común es distinguir habilidad, estrategia y azar sin usar información del resultado para predecirlo.
