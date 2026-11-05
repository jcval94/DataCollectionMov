# Catálogo de datasets reales de México y fuentes globales sorprendentes

Revisión: **4 de noviembre de 2026**, zona `America/Mexico_City`. Repositorio: `jcval94/DataCollectionMov`.

45 fichas de datasets, productos y fuentes documentales reales. La selección prioriza preguntas sobre oportunidades educativas, movilidad, desigualdad territorial y uso de recursos públicos. Incluye fuentes del sorteo alusivo al avión presidencial.

**Alcance:** catálogo con enlaces y propuestas; las nuevas fuentes todavía no están ingeridas. Sólo se identifican como existentes las integraciones comprobadas en el código y el árbol del repo. La ampliación incorpora pruebas públicas acotadas, sin credenciales personales; no es una ingesta masiva ni una evaluación de la salud de los workflows.

- [Versión estructurada JSON](../catalogs/datasets_reales_mexico.json): mismos 45 registros, fuentes, acceso, periodicidad, variables, llaves de cruce y limitaciones.
- [Tablas operativas existentes](tablas.md) y [configuración de recolección](../configs/tables.yml): describen las extracciones ya implementadas; este catálogo no las modifica.

## Por dónde empezaría

Estas prioridades son recomendaciones de análisis, no resultados calculados ni compromisos de ingesta.

| Orden | Conjunto de fuentes | Pregunta y visualización sugerida | Motivo |
| --- | --- | --- | --- |
| 1 | Censo AGEB/manzana + Marco Geoestadístico + Metrobús + DENUE | ¿Dónde hay población en edad escolar y poca accesibilidad a escuelas? Mapa de cobertura y barras por zona. | Aprovecha las extracciones del repo y añade contexto poblacional. |
| 2 | SEPOMEX + polígonos CP CDMX + DENUE + CLUES | ¿Qué CP tienen menor oferta cercana de escuelas y salud? Mapa y ranking con denominador explícito. | Construye una base territorial reutilizable. |
| 3 | CCT + Formato 911 + Metrobús | ¿Qué escuelas con más matrícula tienen conexiones limitadas? Mapa y dispersión matrícula–accesibilidad. | Vincula transporte con demanda educativa observada. |
| 4 | PEF + Cuenta Pública + SRFT + pobreza municipal | ¿Cómo se asigna y ejerce el gasto frente a las carencias? Barras aprobado/modificado/devengado y mapa por habitante. | Separa asignación de ejecución y ubicación del gasto. |
| 5 | EMOVI 2023 + EMOVI 2017 + MMSI, analizadas por separado | ¿Cuánto pesa el origen en el destino educativo y económico? Matrices de transición ponderadas. | Permite estudiar movilidad social sin inferirla sólo de mapas. |
| 6 | ENIGH 2024 + EOD 2017, mediante agregados compatibles | ¿Qué proporción del ingreso absorbe trasladarse o estudiar? Distribuciones ponderadas. | Une la dimensión monetaria con patrones de traslado históricos. |
| 7 | GSE 235: auditoría ASF + balances + lista oficial cuando se recupere | ¿Cómo concilian ventas, premios y remanentes entre documentos? Tabla de conciliación y flujo financiero por corte. | Caso acotado de trazabilidad y calidad documental. |

## Cómo interpretar la verificación

- **Contenido primario leído:** se recuperó contenido de la página o documento. No acredita que todos sus archivos se descarguen.
- **Fuente primaria indexada:** una búsqueda devolvió la ficha del productor; el archivo de datos no se probó.
- **Fuente indexada; apertura fallida:** hubo 403, 502, timeout u otro fallo del entorno. No implica que la fuente haya desaparecido ni que esté disponible para automatización.
- **Código y árbol revisados:** se comprobó implementación en este repo, sin ejecutar credenciales ni afirmar que el servicio responda hoy.

Las variables son una selección conceptual, no un diccionario de columnas extraído de todos los archivos. Las llaves son propuestas de enlace; su unicidad debe comprobarse. La fecha de revisión del catálogo no es la fecha del último dato. `Baja/Media/Alta` estima esfuerzo de incorporación.

## DOF, fuentes sorprendentes y pruebas

El DOF se usa para explicar Git con una reforma real y una [demostración ejecutable de dos commits](../examples/dof_git/README.md). La selección global incorpora señales científicas, biodiversidad, audio, imágenes, literatura, noticias y relatos de avistamientos. Cada ficha distingue contenido **estructurado**, **no estructurado** o **mixto**, además de su formato.

- [README de las pruebas y ejemplos reales](../source_tests/README.md).
- [Resultados HTTP y muestras en JSON](../source_tests/results.json).
- [Definición de las 45 pruebas](../catalogs/source_probes.json) y [programa reproducible](../scripts/probe_catalog_sources.py).

La verificación inicial de cada ficha se conserva como antecedente de localización. El README de pruebas contiene el estado de acceso medido y fechado; se distingue de ese antecedente y de la periodicidad del fenómeno.


## Índice

| ID | Fuente | Contenido | Prioridad / esfuerzo | CP |
| --- | --- | --- | --- | --- |
| [rifa-235-premios](#rifa-235-premios) | GSE 235: lista oficial de premios | no_estructurado | P2 / Alta | No asumir |
| [rifa-235-reportes](#rifa-235-reportes) | GSE 235: balance y beneficiarios publicados | mixto | P2 / Media | No asumir |
| [rifa-235-asf](#rifa-235-asf) | GSE 235: auditoría de gestión financiera | mixto | P1 / Media | No asumir |
| [inegi-indicadores-api](#inegi-indicadores-api) | API del Banco de Indicadores | estructurado | P1 / Baja | No asumir |
| [inegi-denue](#inegi-denue) | DENUE: establecimientos y actividad económica | estructurado | P1 / Baja | Campo documentado |
| [inegi-censo-2020-ageb](#inegi-censo-2020-ageb) | Censo 2020: indicadores por AGEB y manzana urbana | estructurado | P1 / Media | Cruce espacial |
| [inegi-marco-geoestadistico](#inegi-marco-geoestadistico) | Marco Geoestadístico y equivalencias | estructurado | P1 / Media | Cruce espacial |
| [inegi-entorno-urbano-2020](#inegi-entorno-urbano-2020) | Características del entorno urbano 2020 | mixto | P2 / Media | Cruce espacial |
| [inegi-enigh-2024](#inegi-enigh-2024) | ENIGH 2024: ingresos y gastos del hogar | estructurado | P1 / Media | No asumir |
| [inegi-enoe](#inegi-enoe) | ENOE: empleo, ingresos laborales e informalidad | estructurado | P2 / Media | No asumir |
| [inegi-eod-zmvm-2017](#inegi-eod-zmvm-2017) | Encuesta Origen Destino ZMVM 2017 | estructurado | P1 / Media | No asumir |
| [sepomex-codigos-postales](#sepomex-codigos-postales) | Catálogo Nacional de Códigos Postales | estructurado | P1 / Baja | Catálogo |
| [cdmx-codigos-postales-poligonos](#cdmx-codigos-postales-poligonos) | Códigos postales CDMX: capa geográfica | estructurado | P1 / Baja | Polígonos |
| [shcp-pef](#shcp-pef) | Presupuesto de Egresos de la Federación aprobado | mixto | P1 / Media | No asumir |
| [shcp-cuenta-publica](#shcp-cuenta-publica) | Cuenta Pública: gasto al cierre | mixto | P1 / Media | No asumir |
| [shcp-srft](#shcp-srft) | SRFT: ejercicio y destino del gasto federalizado | mixto | P1 / Alta | Cruce espacial |
| [sep-cct](#sep-cct) | Catálogo de Centros de Trabajo | estructurado | P1 / Media | Por confirmar |
| [sep-formato-911](#sep-formato-911) | Formato 911: alumnado, docentes y escuelas | estructurado | P1 / Media | Por confirmar |
| [anuies-anuario](#anuies-anuario) | Anuario Estadístico de Educación Superior | estructurado | P2 / Media | No asumir |
| [ceey-emovi-2023](#ceey-emovi-2023) | ESRU–EMOVI 2023 | estructurado | P1 / Media | No asumir |
| [ceey-emovi-2017](#ceey-emovi-2017) | ESRU–EMOVI 2017 | estructurado | P1 / Media | No asumir |
| [inegi-mmsi-2016](#inegi-mmsi-2016) | Módulo de Movilidad Social Intergeneracional 2016 | estructurado | P2 / Media | No asumir |
| [coneval-pobreza-municipal](#coneval-pobreza-municipal) | Pobreza municipal 2010–2020 | estructurado | P1 / Baja | No asumir |
| [conapo-marginacion-2020](#conapo-marginacion-2020) | Índices de marginación 2020 | estructurado | P1 / Baja | Cruce espacial |
| [metrobus-gtfs](#metrobus-gtfs) | Metrobús: GTFS estático y tiempo real | estructurado | P1 / Baja | Cruce espacial |
| [ecobici-viajes](#ecobici-viajes) | ECOBICI: viajes históricos | estructurado | P1 / Baja | Cruce espacial |
| [ecobici-gbfs](#ecobici-gbfs) | ECOBICI: catálogo y disponibilidad GBFS | estructurado | P2 / Baja | Cruce espacial |
| [salud-clues](#salud-clues) | CLUES: establecimientos de salud | estructurado | P1 / Baja | Campo documentado |
| [cdmx-fgj-carpetas](#cdmx-fgj-carpetas) | Carpetas de investigación FGJ CDMX | estructurado | P2 / Media | Cruce espacial |
| [inegi-atus](#inegi-atus) | ATUS: accidentes de tránsito urbanos y suburbanos | estructurado | P2 / Media | Cruce espacial |
| [dof-publicaciones](#dof-publicaciones) | DOF/SIDOF: publicaciones y reformas para explicar Git | mixto | P2 / Media | No asumir |
| [usgs-sismos](#usgs-sismos) | Terremotos del último día y sus revisiones | estructurado | P2 / Media | No asumir |
| [nasa-exoplanetas](#nasa-exoplanetas) | Planetas fuera del Sistema Solar | estructurado | P2 / Media | No asumir |
| [gwosc-ondas-gravitacionales](#gwosc-ondas-gravitacionales) | Colisiones de agujeros negros y ondas gravitacionales | mixto | P2 / Media | No asumir |
| [noaa-ghcn](#noaa-ghcn) | El clima escrito por estaciones meteorológicas | estructurado | P2 / Media | No asumir |
| [gbif-biodiversidad](#gbif-biodiversidad) | Dónde se ha observado vida: especies y sesgo de muestreo | mixto | P2 / Media | No asumir |
| [xeno-canto-audio](#xeno-canto-audio) | Cantos de aves, murciélagos e insectos | mixto | P2 / Media | No asumir |
| [met-arte](#met-arte) | Arte, objetos e imágenes del Metropolitan Museum | mixto | P2 / Media | No asumir |
| [loc-prensa-historica](#loc-prensa-historica) | Periódicos antiguos: portadas, OCR y metadatos | mixto | P2 / Media | No asumir |
| [gutenberg-quijote](#gutenberg-quijote) | Don Quijote como corpus de lenguaje | no_estructurado | P2 / Media | No asumir |
| [openfoodfacts-alimentos](#openfoodfacts-alimentos) | Alimentos: ingredientes, nutrientes y fotos de etiquetas | mixto | P2 / Media | No asumir |
| [nuforc-ovnis](#nuforc-ovnis) | Relatos de avistamientos de ovnis/UAP | mixto | P2 / Media | No asumir |
| [gdelt-noticias](#gdelt-noticias) | El mundo contado por noticias: eventos y menciones | mixto | P2 / Media | No asumir |
| [nasa-bolidos](#nasa-bolidos) | Bólidos: entradas atmosféricas detectadas por sensores | estructurado | P2 / Media | No asumir |
| [nyc-ratas](#nyc-ratas) | Inspecciones de ratas por predio en Nueva York | mixto | P2 / Media | Campo documentado |

## Reglas para combinar los datos

1. **CP como texto:** preservar cinco dígitos. Un CP puede tener varios asentamientos. CP, colonia, municipio, distrito EOD y AGEB son unidades distintas.
2. **Cruces espaciales:** usar coordenadas y polígonos con CRS y edición compatibles. Registrar puntos sin correspondencia y fronteras ambiguas. Repartir población entre CP y AGEB requiere una regla de ponderación; una intersección geométrica no basta.
3. **Encuestas:** usar factores, estratos y conglomerados donde corresponda. ENIGH, ENOE, EMOVI y MMSI no autorizan estimaciones por CP. No vincular entrevistados de encuestas u olas diferentes como si fueran la misma persona.
4. **Presupuesto:** conservar ejercicio, clasificación y momento contable. No sumar aprobado con pagado ni trimestres acumulados. Para comparar años, deflactar con una serie documentada. Una oficina ejecutora no identifica al beneficiario territorial.
5. **Tiempo:** Censo 2020, EOD 2017 y encuestas retrospectivas representan sus periodos. Combinar con snapshots actuales produce un análisis con bases históricas, que debe declararse.
6. **Educación:** una unidad DENUE no equivale siempre a CCT; el turno/servicio puede duplicar un inmueble. No interpretar matrícula como aprendizaje ni egresados/matrícula como tasa longitudinal.

## Caso especial: rifa del avión presidencial

Separar tres objetos: **lista de billetes premiados**, **reportes de balance/beneficiarios** y **auditoría financiera**. La rifa es el Gran Sorteo Especial 235 de 2020, alusivo al valor del avión; no confundir con la venta de la aeronave.

La auditoría [51-GB, Cuenta Pública 2020](https://www.asf.gob.mx/Trans/Informes/IR2020c/Documentos/Auditorias/2020_0051_a.pdf), resultado 4, ofrece tablas consultables. La lista histórica de premios sigue pendiente de recuperar. Conservar documento, página, fecha de corte y unidad; las discrepancias entre comunicados y auditoría requieren conciliación, no sustitución silenciosa.

Esquema **propuesto**, todavía sin registros extraídos:

- `rifa_documentos`: identificador, productor, URL, publicación, corte, página y hash del archivo recuperado.
- `rifa_conceptos`: documento, concepto, valor literal, unidad original y monto normalizado.
- `rifa_premios`: sorteo, billete, premio, condición de cobro y documento de respaldo; usar nulos cuando no se conozcan.
- `rifa_instituciones`: institución mencionada y correspondencia CCT/CLUES sólo si se verifica.


## Fichas

### Rifa del avión

#### rifa-235-premios

**GSE 235: lista oficial de premios** — Lotería Nacional.

- **Contenido:** no_estructurado; modalidades: text.
- **Cobertura y unidad:** México. Billete premiado.
- **Periodo / actualización:** 15-09-2020. Evento único.
- **Acceso y formatos:** Recuperar PDF histórico citado; requiere extracción y revisión manual. Formatos: PDF.
- **Variables de interés:** Número de billete; Premio; Número y fecha de sorteo.
- **Llaves propuestas:** sorteo + número de billete (texto, conservar longitud).
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Alta.
- **Integración:** `not_ingested`.
- **Análisis:** Distribución de números ganadores y simulación del sorteo.
- **Límites:** PDF no recuperado en esta revisión; no existe CSV validado en el repo. Lista de ganadores no equivale a registro de ventas ni de cobro; no permite atribuir irregularidades.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [rifa-235-premios](../source_tests/README.md#rifa-235-premios).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.gob.mx/lotenal/prensa/con-gran-apoyo-de-la-sociedad-lotenal-llevo-a-cabo-con-exito-el-gran-sorteo-especial-no-235?idiom=es-MX) — `indexed_primary_fetch_blocked`. Comunicado oficial indexado; apertura devolvió 403. Cita la lista en http://www.lotenal.gob.mx/Comercial/Listas/235.pdf; la variante HTTPS no pudo recuperarse. [Recurso localizado](http://www.lotenal.gob.mx/Comercial/Listas/235.pdf).

#### rifa-235-reportes

**GSE 235: balance y beneficiarios publicados** — Lotería Nacional / INDEP.

- **Contenido:** mixto; modalidades: text, tabular.
- **Cobertura y unidad:** México; instituciones mencionadas. Concepto financiero o institución, separado por documento.
- **Periodo / actualización:** Comunicados de 2020. Evento único; reportes con diferentes cortes.
- **Acceso y formatos:** Reconstrucción documental; no hay microdatos completos de ventas verificados. Formatos: HTML.
- **Variables de interés:** Ventas; Premios; Gastos; Remanente; Instituciones reportadas.
- **Llaves propuestas:** documento + fecha de publicación + concepto; CCT/CLUES sólo tras correspondencia documentada.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Comparar balances por fecha; documentar escuelas beneficiarias.
- **Límites:** Separar cortes y definiciones: las cifras iniciales y auditadas pueden diferir. Una escuela mencionada no trae necesariamente CCT; vincular sólo con evidencia.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [rifa-235-reportes](../source_tests/README.md#rifa-235-reportes).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.gob.mx/lotenal/prensa/197193) — `indexed_primary_fetch_blocked`. Comunicado del 11-12-2020 indexado; apertura devolvió 403.
- [Fuente 2](https://www.gob.mx/indep/prensa/informa-indep-que-siete-escuelas-recibieron-premios-del-sorteo-alusivo-al-avion-presidencial) — `indexed_primary`. Comunicado oficial localizado en el índice de búsqueda; archivo tabular no comprobado.

#### rifa-235-asf

**GSE 235: auditoría de gestión financiera** — Auditoría Superior de la Federación.

- **Contenido:** mixto; modalidades: text, tabular.
- **Cobertura y unidad:** México. Concepto o categoría del resultado 4.
- **Periodo / actualización:** Cuenta Pública 2020; revisión posterior. Informe histórico.
- **Acceso y formatos:** PDF público legible; extraer tablas de las páginas impresas 23–31. Formatos: PDF.
- **Variables de interés:** Billetes vendidos y no vendidos; Tipo de ganador; Premios pagados; Flujos y rentabilidad.
- **Llaves propuestas:** auditoría + página + concepto + unidad.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Conciliar ventas, premios y remanentes contra los comunicados.
- **Límites:** El PDF contiene discrepancias internas: conservar página, unidad y literal original. Importes expresados en miles de pesos; distinguirlos de pesos.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [rifa-235-asf](../source_tests/README.md#rifa-235-asf).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.asf.gob.mx/Trans/Informes/IR2020c/Documentos/Auditorias/2020_0051_a.pdf) — `opened_primary`. PDF legible de 68 páginas; resultado 4, páginas impresas 23–31, dedicado al GSE 235. [Recurso localizado](https://www.asf.gob.mx/Trans/Informes/IR2020c/Documentos/Auditorias/2020_0051_a.pdf).

### INEGI y contexto

#### inegi-indicadores-api

**API del Banco de Indicadores** — INEGI.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** México; geografía disponible según indicador. Indicador × área × periodo.
- **Periodo / actualización:** Series variables según indicador. Según indicador.
- **Acceso y formatos:** API con token INEGI; seleccionar IDs mediante catálogo de metadatos. Formatos: JSON, XML.
- **Variables de interés:** ID de indicador; Periodo; Valor; Unidad; Área geográfica.
- **Llaves propuestas:** ID indicador + área + periodo + fuente/versión.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Integración:** `not_ingested`.
- **Análisis:** Series de población, precios o actividad para contextualizar transporte y gasto.
- **Límites:** No todos los indicadores admiten municipio o AGEB. Guardar unidad, base, frecuencia, fuente y revisiones; no asumir que el token DENUE sirve sin comprobar.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.
- **Prueba y ejemplos:** [inegi-indicadores-api](../source_tests/README.md#inegi-indicadores-api).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.inegi.org.mx/servicios/api-indicadores/) — `opened_primary`. Documentación de indicadores y catálogo de metadatos leída. No se ejecutaron consultas con token.

#### inegi-denue

**DENUE: establecimientos y actividad económica** — INEGI.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** Nacional; extracción actual centrada en educación CDMX. Establecimiento por edición/snapshot.
- **Periodo / actualización:** Edición vigente y snapshots propios. Ediciones del productor; consulta mensual en este repo.
- **Acceso y formatos:** API con token; ampliar sectores o estados cuando se implemente. Formatos: JSON API, Descarga masiva.
- **Variables de interés:** CLEE/ID; Actividad SCIAN; Estrato de personal; CP; Latitud y longitud.
- **Llaves propuestas:** CLEE o ID establecimiento + edición; CP como agrupación; coordenadas para cruce espacial.
- **CP:** Campo documentado. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Integración:** `partial`. Rutas: [`src/historico_api/sources/denue.py`](../src/historico_api/sources/denue.py), [`data/current/denue_cdmx_sector_61_servicios_educativos.csv`](../data/current/denue_cdmx_sector_61_servicios_educativos.csv).
- **Análisis:** Mapear servicios y concentración de escuelas por CP y acceso al Metrobús.
- **Límites:** Estrato de personal no es facturación ni empleo exacto. La integración actual no cubre todo DENUE; usar ID/CLEE y edición al deduplicar.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.
- **Prueba y ejemplos:** [inegi-denue](../source_tests/README.md#inegi-denue).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.inegi.org.mx/servicios/api-denue/) — `indexed_primary_fetch_blocked`. Documentación oficial indexada con campo CP; apertura devolvió 502. Integración y campo cp confirmados en el código del repo.

#### inegi-censo-2020-ageb

**Censo 2020: indicadores por AGEB y manzana urbana** — INEGI.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** México; resultados urbanos a pequeña área. Área geográfica × indicador; separar agregados.
- **Periodo / actualización:** 2020. Censal; puede haber correcciones del archivo.
- **Acceso y formatos:** Descarga desde programa CPV 2020; seleccionar resultados AGEB/manzana urbana. Formatos: CSV/ZIP, Diccionario.
- **Variables de interés:** Población; Edad; Escolaridad; Discapacidad; Vivienda.
- **Llaves propuestas:** Entidad (2) + municipio (3) + localidad (4) + AGEB (4); manzana (3) cuando proceda.
- **CP:** Cruce espacial. **Prioridad:** P1. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Estimar población y rezago educativo cerca de estaciones y escuelas.
- **Límites:** CP no es AGEB; manejar asteriscos y valores reservados como faltantes. No sumar filas totales con manzanas; mantener claves geográficas como texto.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.
- **Prueba y ejemplos:** [inegi-censo-2020-ageb](../source_tests/README.md#inegi-censo-2020-ageb).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.inegi.org.mx/programas/ccpv/2020/) — `indexed_primary`. Programa oficial y disponibilidad de resultados por AGEB/manzana localizados. La ficha antigua tit=326085 devolvió 'archivo no existe'; usar el programa como entrada.

#### inegi-marco-geoestadistico

**Marco Geoestadístico y equivalencias** — INEGI.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** Nacional. Polígono, localidad o clave por edición.
- **Periodo / actualización:** Edición compatible con el dato analizado; 2020 para Censo 2020. Actualizaciones por edición.
- **Acceso y formatos:** Descargar edición y entidad desde portal oficial. Formatos: SHP/ZIP, Catálogos.
- **Variables de interés:** CVEGEO; Entidad; Municipio; Localidad; AGEB; Geometría.
- **Llaves propuestas:** CVEGEO + edición + nivel.
- **CP:** Cruce espacial. **Prioridad:** P1. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Unir censo con estaciones, escuelas, CP y presupuesto territorial.
- **Límites:** Fijar edición y CRS; cambios de límites requieren equivalencias. Geografía estadística no equivale automáticamente a límite jurídico.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.
- **Prueba y ejemplos:** [inegi-marco-geoestadistico](../source_tests/README.md#inegi-marco-geoestadistico).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.inegi.org.mx/temas/mg/) — `indexed_primary`. Portal oficial de descargas y metadatos del Marco Geoestadístico localizados.

#### inegi-entorno-urbano-2020

**Características del entorno urbano 2020** — INEGI.

- **Contenido:** mixto; modalidades: text, tabular.
- **Cobertura y unidad:** Localidades urbanas cubiertas por el levantamiento. Manzana y vialidad, tablas distintas.
- **Periodo / actualización:** 2020. Levantamiento 2020.
- **Acceso y formatos:** Microdatos del CPV 2020 enlazados en metadatos oficiales. Formatos: Bases descargables, Diccionario XLSX.
- **Variables de interés:** Banquetas; Rampas; Alumbrado; Características viales.
- **Llaves propuestas:** Clave geográfica de manzana/vialidad según diccionario + edición.
- **CP:** Cruce espacial. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Accesibilidad peatonal en el entorno de escuelas y estaciones.
- **Límites:** Revisar categorías y cobertura exacta de cada variable. Infraestructura registrada en 2020 no describe necesariamente el estado actual.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.
- **Prueba y ejemplos:** [inegi-entorno-urbano-2020](../source_tests/README.md#inegi-entorno-urbano-2020).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.inegi.org.mx/rnm/index.php/catalog/941/related-materials) — `indexed_primary`. Metadatos oficiales identifican tablas de Vialidad y Manzana y enlazan los microdatos del CPV 2020.

#### inegi-enigh-2024

**ENIGH 2024: ingresos y gastos del hogar** — INEGI.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** Nacional y dominios de estimación de la encuesta. Vivienda, hogar, persona, ingreso o gasto; tablas relacionadas.
- **Periodo / actualización:** 2024; ediciones anteriores en el programa. Bienal.
- **Acceso y formatos:** Microdatos públicos por edición. Formatos: CSV/ZIP, Documentación.
- **Variables de interés:** Ingreso corriente; Gasto en transporte; Gasto educativo; Composición del hogar.
- **Llaves propuestas:** folioviv + foliohog; numren en tablas de personas, según diccionario; Entidad para agregados representativos.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Carga del transporte y educación sobre el ingreso, por decil y entidad.
- **Límites:** Usar ponderadores, estratos y UPM; no estimar por CP o manzana. Es corte transversal: no mide por sí sola movilidad intergeneracional.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.
- **Prueba y ejemplos:** [inegi-enigh-2024](../source_tests/README.md#inegi-enigh-2024).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.inegi.org.mx/programas/enigh/nc/2024/) — `indexed_primary`. Programa oficial, microdatos y documentación ENIGH 2024 localizados.

#### inegi-enoe

**ENOE: empleo, ingresos laborales e informalidad** — INEGI.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** Nacional, entidades y ciudades autorrepresentadas según edición. Persona y hogar por trimestre.
- **Periodo / actualización:** Desde 2005; seleccionar trimestre disponible. Indicadores mensuales y trimestrales; microdatos por corte.
- **Acceso y formatos:** Microdatos públicos; fijar periodo y versión. Formatos: CSV/DBF según edición, Documentación.
- **Variables de interés:** Escolaridad; Ocupación; Horas; Ingreso laboral; Informalidad.
- **Llaves propuestas:** Llaves de vivienda/hogar/persona y trimestre según diccionario.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Brechas laborales por escolaridad, edad y género.
- **Límites:** Diseño muestral y cambios durante pandemia requieren tratamiento. No unir personas entre encuestas distintas; no inferir salarios por CP.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.
- **Prueba y ejemplos:** [inegi-enoe](../source_tests/README.md#inegi-enoe).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.inegi.org.mx/programas/enoe/15ymas/) — `indexed_primary`. Programa oficial y notas sobre revisiones de microdatos localizados; no se determinó el último trimestre descargable.

#### inegi-eod-zmvm-2017

**Encuesta Origen Destino ZMVM 2017** — INEGI / gobiernos CDMX y Estado de México.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** ZMVM dentro de la cobertura de la encuesta. Hogar, persona y viaje.
- **Periodo / actualización:** 2017. Levantamiento específico.
- **Acceso y formatos:** Descarga por programa; revisar distritos y factores. Formatos: Microdatos, Tabulados, Cartografía/documentación.
- **Variables de interés:** Origen/destino; Motivo; Modo; Tiempo; Costo.
- **Llaves propuestas:** Identificadores de hogar/persona/viaje y distrito según diccionario.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Viajes a estudiar; carga de traslado y conexiones con transporte público.
- **Límites:** Distritos EOD no son CP; revisar cartografía y dominios. La red y los patrones de 2017 son una referencia histórica.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.
- **Prueba y ejemplos:** [inegi-eod-zmvm-2017](../source_tests/README.md#inegi-eod-zmvm-2017).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.inegi.org.mx/programas/eod/2017/default.html) — `indexed_primary`. Programa oficial de la EOD ZMVM 2017 y catálogo de microdatos localizados.

### Código postal y territorio

#### sepomex-codigos-postales

**Catálogo Nacional de Códigos Postales** — Servicio Postal Mexicano.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** México. Asentamiento × CP; un CP puede tener varios asentamientos.
- **Periodo / actualización:** Corte del archivo descargado. Actualización del productor, sin calendario validado.
- **Acceso y formatos:** Exportación por entidad o país en formulario; descarga no probada. Formatos: TXT, Excel/XML según formulario.
- **Variables de interés:** CP; Asentamiento; Tipo de asentamiento; Municipio; Entidad.
- **Llaves propuestas:** CP + identificador de asentamiento; validar unicidad; Claves de entidad/municipio previa homologación.
- **CP:** Catálogo. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Integración:** `not_ingested`.
- **Análisis:** Normalizar domicilios y explorar desigualdad de servicios por CP.
- **Límites:** Conservar CP como texto de cinco dígitos, incluidos ceros iniciales. No ofrece por sí solo polígonos ni relación uno a uno CP–municipio.
- **Uso:** La consulta oficial indica gratuidad y prohíbe comercialización total o parcial del catálogo; revisar aviso antes de redistribuir.
- **Prueba y ejemplos:** [sepomex-codigos-postales](../source_tests/README.md#sepomex-codigos-postales).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx) — `indexed_primary_fetch_blocked`. Página oficial de exportación localizada; apertura agotó el tiempo. El formulario y sus descargas no se probaron.

#### cdmx-codigos-postales-poligonos

**Códigos postales CDMX: capa geográfica** — Gobierno de la Ciudad de México.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** Ciudad de México. Polígono de código postal.
- **Periodo / actualización:** Edición del recurso; no determinada en esta revisión. Sin calendario validado.
- **Acceso y formatos:** Recurso geográfico desde ficha CKAN; descarga pendiente. Formatos: GeoJSON.
- **Variables de interés:** Código postal; Geometría.
- **Llaves propuestas:** CP (texto); unión espacial punto–polígono.
- **CP:** Polígonos. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Integración:** `not_ingested`.
- **Análisis:** Asignar CP a establecimientos, estaciones y unidades de salud por coordenadas.
- **Límites:** Revisar CRS, geometrías, solapes y fecha de corte. Un polígono CP no reproduce una AGEB; no agregar población sin regla espacial explícita.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [cdmx-codigos-postales-poligonos](../source_tests/README.md#cdmx-codigos-postales-poligonos).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.datos.cdmx.gob.mx/es_AR/dataset/codigos-postales) — `indexed_primary`. Ficha oficial indexada anuncia GeoJSON. La variante /dataset/codigos-postales agotó el tiempo; geometrías no descargadas.

### Presupuesto

#### shcp-pef

**Presupuesto de Egresos de la Federación aprobado** — SHCP.

- **Contenido:** mixto; modalidades: text, tabular.
- **Cobertura y unidad:** Federal; entidad cuando el registro la desagrega. Clave presupuestaria × ejercicio.
- **Periodo / actualización:** PEF 2026 identificado; otros ejercicios según portal. Anual.
- **Acceso y formatos:** Ficha y analíticos oficiales; descarga bloqueada durante esta revisión. Formatos: Bases tabulares, Catálogos, Analíticos.
- **Variables de interés:** Ramo; Unidad responsable; Programa; Objeto/tipo de gasto; Monto aprobado.
- **Llaves propuestas:** Ejercicio + clave presupuestaria completa del recurso.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Asignación a educación, salud y movilidad por programa y habitante.
- **Límites:** PPEF es propuesta; PEF es aprobado: nunca intercambiarlos. Ubicación presupuestaria puede ser unidad ejecutora y no beneficiarios; homogeneizar pesos reales.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [shcp-pef](../source_tests/README.md#shcp-pef).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.datos.gob.mx/dataset/presupuesto_egresos_federacion_pef) — `indexed_primary_fetch_blocked`. Ficha oficial indexada describe el PEF 2026; apertura devolvió 403. El portal de analíticos devolvió 502.
- [Fuente 2](https://www.pef.hacienda.gob.mx/es/PEF/Analiticos_PresupuestariosPEF) — `indexed_primary_fetch_blocked`. Ruta oficial de analíticos localizada en búsqueda; apertura devolvió 502.

#### shcp-cuenta-publica

**Cuenta Pública: gasto al cierre** — SHCP.

- **Contenido:** mixto; modalidades: text, tabular.
- **Cobertura y unidad:** Federal y desagregaciones de la base elegida. Clave presupuestaria × ejercicio × momento contable.
- **Periodo / actualización:** Cuenta Pública 2025 identificada. Anual.
- **Acceso y formatos:** Datos abiertos del ejercicio y sus catálogos; descarga pendiente. Formatos: Bases tabulares, Reportes.
- **Variables de interés:** Aprobado; Modificado; Devengado; Pagado; Programa.
- **Llaves propuestas:** Ejercicio + clave presupuestaria + momento contable.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Diferencia entre asignación y gasto al cierre por sector.
- **Límites:** Homologar llaves y clasificaciones entre ejercicios. Devengado y pagado son conceptos distintos; no sumar momentos contables.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [shcp-cuenta-publica](../source_tests/README.md#shcp-cuenta-publica).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.transparenciapresupuestaria.gob.mx/es/PTP/Cuenta_Publica_2025) — `indexed_primary_fetch_blocked`. Página oficial indexada con datos abiertos; apertura devolvió 502.

#### shcp-srft

**SRFT: ejercicio y destino del gasto federalizado** — SHCP y gobiernos subnacionales.

- **Contenido:** mixto; modalidades: text, tabular.
- **Cobertura y unidad:** Entidades y municipios; proyectos con georreferencia cuando exista. Ejercicio: registro presupuestario; destino: proyecto/ubicación × corte.
- **Periodo / actualización:** Ejercicios y trimestres publicados; último corte no comprobado. Trimestral.
- **Acceso y formatos:** Descargar separadamente Ejercicio del gasto y Destino del gasto. Formatos: Bases tabulares, Anexos.
- **Variables de interés:** Fondo; Municipio; Proyecto; Avance físico/financiero; Coordenadas si existen.
- **Llaves propuestas:** Ejercicio + trimestre + fondo + entidad/municipio; folio de proyecto en Destino.
- **CP:** Cruce espacial. **Prioridad:** P1. **Esfuerzo:** Alta.
- **Integración:** `not_ingested`.
- **Análisis:** Priorizar zonas con carencias y obras rezagadas; gasto escolar y accesibilidad.
- **Límites:** No sumar cortes acumulados trimestrales ni multiplicar monto al expandir ubicaciones. Coordenadas faltantes o de oficina requieren validar destino; no asumir CP nativo.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [shcp-srft](../source_tests/README.md#shcp-srft).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.transparenciapresupuestaria.gob.mx/Entidades-Federativas) — `indexed_primary_fetch_blocked`. Página oficial indexada describe ejercicio, destino y resultados trimestrales; apertura devolvió 502.
- [Fuente 2](https://www.finanzaspublicas.hacienda.gob.mx/es/Finanzas_Publicas/Informes_al_Congreso_de_la_Union) — `indexed_primary`. Página SHCP localizada con el informe de recursos federales transferidos y sus carpetas.

### Educación

#### sep-cct

**Catálogo de Centros de Trabajo** — SEP / SIGED.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** México. Centro de trabajo; revisar servicios y turnos del archivo.
- **Periodo / actualización:** Corte publicado por SIGED; no determinado. Actualización del catálogo; sin frecuencia comprobada.
- **Acceso y formatos:** SIGED anuncia la descarga; los recursos no fueron visibles en lectura estática. Formatos: Descarga anunciada; formato por confirmar.
- **Variables de interés:** CCT; Nombre; Nivel/servicio; Sostenimiento; Ubicación según archivo.
- **Llaves propuestas:** CCT + turno/servicio cuando aplique + corte.
- **CP:** Por confirmar. **Prioridad:** P1. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Escuelas con baja accesibilidad; cobertura educativa por territorio.
- **Límites:** Confirmar CP y coordenadas en el diccionario antes de tratarlos como disponibles. CCT, turno y servicio pueden producir varias filas por inmueble.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [sep-cct](../source_tests/README.md#sep-cct).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://siged.sep.gob.mx/SIGED/datos_abiertos.html) — `opened_primary`. Página oficial leída; anuncia Catálogo de Centros de Trabajo y Formato 911. Las tablas de descarga no expusieron archivos en la lectura estática.

#### sep-formato-911

**Formato 911: alumnado, docentes y escuelas** — SEP.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** México, conforme recursos y ciclo. Escuela/servicio o agregado, según archivo × ciclo.
- **Periodo / actualización:** Ciclos disponibles en la fuente; último no determinado. Por ciclo escolar.
- **Acceso y formatos:** Seleccionar recurso por nivel y ciclo en datos.gob.mx o SIGED. Formatos: Bases tabulares, Diccionario.
- **Variables de interés:** Matrícula; Docentes; Grupos; Nivel y modalidad.
- **Llaves propuestas:** Ciclo + CCT/turno/servicio si el recurso los contiene.
- **CP:** Por confirmar. **Prioridad:** P1. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Razón alumnos/docente y oferta educativa vinculada a transporte.
- **Límites:** No son expedientes individuales de alumnos. Confirmar CCT, granularidad y turnos antes de enlazar; matrícula no mide calidad del aprendizaje.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [sep-formato-911](../source_tests/README.md#sep-formato-911).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.datos.gob.mx/dataset/registro_alumnado_personal_docente_educacion_basica_media_superior_formato_911) — `indexed_primary`. Ficha SEP localizada; requiere revisar recursos y diccionario por nivel/ciclo.
- [Fuente 2](https://siged.sep.gob.mx/SIGED/datos_abiertos.html) — `opened_primary`. Página oficial leída; anuncia Catálogo de Centros de Trabajo y Formato 911. Las tablas de descarga no expusieron archivos en la lectura estática.

#### anuies-anuario

**Anuario Estadístico de Educación Superior** — ANUIES.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** México. Institución/plantel × programa × ciclo, según exportación.
- **Periodo / actualización:** Ciclos escolares disponibles en el anuario. Por ciclo escolar.
- **Acceso y formatos:** Filtrar y exportar en aplicación; no asumir API pública. Formatos: Consulta interactiva, Exportaciones por confirmar.
- **Variables de interés:** Programa; Matrícula; Egreso; Titulación; Sexo.
- **Llaves propuestas:** Ciclo + institución/plantel + programa + dimensiones publicadas.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Oferta de carreras y brechas de participación o egreso.
- **Límites:** No dividir egresados entre matrícula como tasa de cohorte. Homologar planteles y carreras; no garantiza CCT o CP.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [anuies-anuario](../source_tests/README.md#anuies-anuario).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://anuario.anuies.mx/) — `indexed_primary`. Aplicación oficial localizada; su enlace fue confirmado en una página de ANUIES abierta. No se exportaron resultados.

### Movilidad social

#### ceey-emovi-2023

**ESRU–EMOVI 2023** — CEEY / Fundación ESRU.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** Nacional, urbano/no urbano y cinco regiones. Persona entrevistada con retrospectiva del hogar de origen.
- **Periodo / actualización:** 2023. Ola específica.
- **Acceso y formatos:** ZIP enlazado desde la página del productor; formato interno no inspeccionado. Formatos: ZIP de bases, Metodología, Programas de cálculo.
- **Variables de interés:** Origen/destino socioeconómico; Educación; Cuidados; Inclusión financiera.
- **Llaves propuestas:** ID de entrevista dentro de la ola; región sólo para agregados.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Matrices de transición y brechas de oportunidades.
- **Límites:** Usar factores y metodología de índices; no extrapolar a CP ni alcaldía. Comparar olas exige armonizar variables.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [ceey-emovi-2023](../source_tests/README.md#ceey-emovi-2023).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://ceey.org.mx/contenido/que-hacemos/emovi/) — `opened_primary`. Página del productor leída y enlace BASES DE DATOS 2023 seguido hasta el ZIP en Drive; contenido del ZIP no descargado. [Recurso localizado](https://drive.google.com/file/d/1r736z5vok0ss68cIW11SnZ5_MR0bUiDC/view?usp=drive_link).

#### ceey-emovi-2017

**ESRU–EMOVI 2017** — CEEY / Fundación ESRU.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** Nacional, cinco regiones y CDMX según diseño. Persona entrevistada y origen familiar retrospectivo.
- **Periodo / actualización:** 2017. Ola específica.
- **Acceso y formatos:** ZIP del productor localizado; contenido no descargado. Formatos: ZIP de bases, Metodología.
- **Variables de interés:** Recursos de origen; Logro educativo; Destino socioeconómico.
- **Llaves propuestas:** ID de entrevista dentro de la ola; dominios sólo para agregados.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Contrastar movilidad regional y CDMX con 2023 donde sea comparable.
- **Límites:** Encuestas independientes; no es panel de las mismas personas. La representatividad CDMX no habilita desglose por CP.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [ceey-emovi-2017](../source_tests/README.md#ceey-emovi-2017).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://ceey.org.mx/contenido/que-hacemos/emovi/) — `opened_primary`. Página del productor leída y enlace BASES DE DATOS 2017 seguido hasta el ZIP en Drive; contenido del ZIP no descargado. [Recurso localizado](https://drive.google.com/file/d/1hko58nfnlexpw5kiB1K0kqeXlOPAaGyr/view?usp=sharing).

#### inegi-mmsi-2016

**Módulo de Movilidad Social Intergeneracional 2016** — INEGI.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** México; dominios definidos por diseño muestral. Persona de 25–64 años, presente y retrospectiva a los 14.
- **Periodo / actualización:** 2016. Levantamiento específico.
- **Acceso y formatos:** Microdatos públicos; tabla MMSI_2016 documentada. Formatos: Microdatos, Diccionario, Cuestionario.
- **Variables de interés:** Educación y ocupación actuales; Condición socioeconómica de origen.
- **Llaves propuestas:** Llave de persona dentro del levantamiento, según diccionario.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Persistencia educativa y ocupacional entre generaciones.
- **Límites:** No mezclar índices MMSI y EMOVI como si fueran equivalentes. Ponderadores y dominios de inferencia obligatorios.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.
- **Prueba y ejemplos:** [inegi-mmsi-2016](../source_tests/README.md#inegi-mmsi-2016).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.inegi.org.mx/programas/mmsi/2016/) — `indexed_primary`. Programa oficial, diccionario y descripción de tabla MMSI_2016 localizados.

#### coneval-pobreza-municipal

**Pobreza municipal 2010–2020** — CONEVAL, archivo histórico.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** Municipios y alcaldías de México. Municipio × año × indicador.
- **Periodo / actualización:** 2010, 2015 y 2020. Cortes de medición publicados.
- **Acceso y formatos:** Descargar bases y metodología del archivo histórico. Formatos: Bases, Programas de cálculo.
- **Variables de interés:** Pobreza; Pobreza extrema; Carencias; Población de referencia.
- **Llaves propuestas:** Clave entidad (2) + municipio (3) + año.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Integración:** `not_ingested`.
- **Análisis:** Distribución de presupuesto por población en pobreza.
- **Límites:** Resultados territoriales, no trayectorias individuales. Revisar cambios municipales y comparabilidad metodológica; no presentar como cifras de 2026.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [coneval-pobreza-municipal](../source_tests/README.md#coneval-pobreza-municipal).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.coneval.org.mx/Medicion/Paginas/Programas_BD_municipal_2010_2020.aspx) — `indexed_primary`. Archivo histórico oficial con bases y programas de cálculo municipal localizado.

#### conapo-marginacion-2020

**Índices de marginación 2020** — CONAPO.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** Entidad, municipio, localidad y ámbito urbano, según base. Área geográfica × indicadores de marginación.
- **Periodo / actualización:** 2020. Edición basada en Censo 2020.
- **Acceso y formatos:** Elegir nivel de desagregación y descargar su base. Formatos: Bases tabulares, Notas técnicas.
- **Variables de interés:** Índice y grado; Indicadores socioeconómicos; Población.
- **Llaves propuestas:** Clave geográfica + nivel + 2020.
- **CP:** Cruce espacial. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Integración:** `not_ingested`.
- **Análisis:** Zonas con marginación alta y baja oferta de transporte o escuelas.
- **Límites:** Marginación y pobreza son medidas distintas. La estimación por colonia no es automáticamente CP; documentar equivalencias.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [conapo-marginacion-2020](../source_tests/README.md#conapo-marginacion-2020).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372) — `indexed_primary`. Página oficial con bases por entidad, municipio, localidad y ámbito urbano localizada.

### Movilidad

#### metrobus-gtfs

**Metrobús: GTFS estático y tiempo real** — Metrobús / proveedor del feed.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** Red Metrobús CDMX. Estación/viaje programado y vehículo × snapshot.
- **Periodo / actualización:** Snapshots propios; disponibilidad según historial del repo. Captura horaria laboral de realtime; estático semanal en configuración.
- **Acceso y formatos:** API autenticada con secrets existentes del repo. Formatos: GTFS ZIP/CSV, GTFS-Realtime protobuf.
- **Variables de interés:** route_id; stop_id; trip_id; Posición; Hora.
- **Llaves propuestas:** _snapshot_id + entity_id; trip_id/route_id/stop_id contra la versión GTFS compatible.
- **CP:** Cruce espacial. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Integración:** `existing`. Rutas: [`src/historico_api/sources/metrobus.py`](../src/historico_api/sources/metrobus.py), [`data/current/metrobus_vehicle_positions.csv`](../data/current/metrobus_vehicle_positions.csv), [`data/current/metrobus_vehicle_positions_enriched.csv`](../data/current/metrobus_vehicle_positions_enriched.csv).
- **Análisis:** Regularidad observada y accesibilidad a escuelas y servicios.
- **Límites:** Snapshots horarios no reconstruyen cada viaje ni miden puntualidad completa. Tablas estáticas configuradas; no todas tenían CSV current en el árbol revisado.
- **Uso:** Revisar condiciones del proveedor para reutilización y redistribución del feed.
- **Prueba y ejemplos:** [metrobus-gtfs](../source_tests/README.md#metrobus-gtfs).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://github.com/jcval94/DataCollectionMov/blob/main/src/historico_api/sources/metrobus.py) — `repository_inspected`. Código de autenticación y recolección leído; rutas de snapshots presentes. No se ejecutó la API autenticada.

#### ecobici-viajes

**ECOBICI: viajes históricos** — ECOBICI / SEMOVI.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** CDMX, área del sistema. Viaje entre cicloestaciones.
- **Periodo / actualización:** Archivos mensuales históricos; página indexa desde 2010. Mensual.
- **Acceso y formatos:** Descarga mensual; recolector ya implementado. Formatos: CSV/ZIP.
- **Variables de interés:** Estaciones de origen/destino; Inicio/fin; Duración; Demografía cuando exista.
- **Llaves propuestas:** ID de estación origen/destino + periodo de vigencia del catálogo.
- **CP:** Cruce espacial. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Integración:** `collector_only`. Rutas: [`src/historico_api/sources/ecobici.py`](../src/historico_api/sources/ecobici.py), [`.github/workflows/ecobici-historical.yml`](../.github/workflows/ecobici-historical.yml).
- **Análisis:** Flujos casa–estudio aproximados y conexiones con Metrobús.
- **Límites:** No se encontró ecobici_historico_normalizado en current durante esta revisión. Cambian esquemas/sistema; una estación cercana a universidad no prueba motivo de viaje.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [ecobici-viajes](../source_tests/README.md#ecobici-viajes).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://ecobici.cdmx.gob.mx/datos-abiertos/) — `indexed_primary`. Página oficial de datos abiertos localizada; histórico mensual también indexado en ecobici.mx/datos-abiertos/.

#### ecobici-gbfs

**ECOBICI: catálogo y disponibilidad GBFS** — ECOBICI / SEMOVI.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** CDMX, cicloestaciones del sistema. Cicloestación × snapshot.
- **Periodo / actualización:** Snapshots propios del repositorio. Disponibilidad en origen en tiempo real; repo cada dos horas laborales.
- **Acceso y formatos:** Feeds GBFS y recolección existentes; consultar configuración actual. Formatos: JSON GBFS, CSV derivado.
- **Variables de interés:** station_id; Capacidad; Bicicletas/espacios disponibles; Coordenadas.
- **Llaves propuestas:** _snapshot_id + station_id.
- **CP:** Cruce espacial. **Prioridad:** P2. **Esfuerzo:** Baja.
- **Integración:** `existing`. Rutas: [`data/current/ecobici_gbfs_station_information.csv`](../data/current/ecobici_gbfs_station_information.csv), [`data/current/ecobici_realtime_stations.csv`](../data/current/ecobici_realtime_stations.csv).
- **Análisis:** Frecuencia observada de estaciones vacías cerca de campus y Metrobús.
- **Límites:** Snapshots no son viajes ni disponibilidad continua. Conservar timestamp y estado operativo al comparar estaciones.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [ecobici-gbfs](../source_tests/README.md#ecobici-gbfs).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://ecobici.cdmx.gob.mx/datos-abiertos/) — `indexed_primary`. Página oficial de datos abiertos localizada; histórico mensual también indexado en ecobici.mx/datos-abiertos/.

### Salud y seguridad

#### salud-clues

**CLUES: establecimientos de salud** — Secretaría de Salud / DGIS.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** México. Establecimiento de salud × corte.
- **Periodo / actualización:** Histórico visible desde 2016; enlace septiembre 2026 localizado. Cortes mensuales publicados.
- **Acceso y formatos:** Descarga del histórico oficial; XLSX localizado, filas no inspeccionadas. Formatos: XLSX.
- **Variables de interés:** CLUES; Institución; Tipo/estatus; CP; Coordenadas según corte.
- **Llaves propuestas:** CLUES + corte; CP como agrupación.
- **CP:** Campo documentado. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Integración:** `not_ingested`.
- **Análisis:** Acceso a unidades de salud por CP y transporte.
- **Límites:** Validar nombres exactos de columnas y unidades activas. Existencia de unidad no implica capacidad, atención efectiva ni calidad.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [salud-clues](../source_tests/README.md#salud-clues).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://gobi.salud.gob.mx/Bases_Clues.html) — `opened_primary`. Histórico oficial leído; enlace septiembre 2026 resolvió a XLSX no interpretable por el navegador de investigación. [Recurso localizado](https://gobi.salud.gob.mx/historico_clues/ESTABLECIMIENTO_SALUD_202609.xlsx?v=1.1).
- [Fuente 2](https://www.dgis.salud.gob.mx/descargas/clues/pdf/Manual_registro_informacion_catalogo_CLUES_202506.pdf) — `opened_primary`. Manual oficial consultado: documenta código postal de cinco dígitos.

#### cdmx-fgj-carpetas

**Carpetas de investigación FGJ CDMX** — FGJ CDMX / portal de datos CDMX.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** Ciudad de México. Registro publicado de carpeta/delito según diccionario.
- **Periodo / actualización:** Desde enero de 2016; último corte sin comprobar. Actualización de la fuente; comprobar corte.
- **Acceso y formatos:** Descarga desde ficha CKAN. Formatos: CSV.
- **Variables de interés:** Delito; Fecha de hechos/apertura; Alcaldía; Colonia; Coordenadas.
- **Llaves propuestas:** ID de registro si existe; fecha y coordenadas para agregados.
- **CP:** Cruce espacial. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Incidencia registrada en entornos de escuelas y estaciones.
- **Límites:** No son todos los delitos: hay subregistro y cambios de clasificación. Usar denominadores de exposición; comparar hechos con hechos y aperturas con aperturas.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.
- **Prueba y ejemplos:** [cdmx-fgj-carpetas](../source_tests/README.md#cdmx-fgj-carpetas).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico) — `indexed_primary`. Ficha FGJ oficial localizada: registros desde enero 2016 y variables geográficas; no se comprobó último mes.

#### inegi-atus

**ATUS: accidentes de tránsito urbanos y suburbanos** — INEGI.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** México; cobertura de reporte y georreferenciación variable. Accidente reportado.
- **Periodo / actualización:** Serie anual; coordenadas desde 2019 en municipios seleccionados. Anual.
- **Acceso y formatos:** Descargar año y diccionario desde programa. Formatos: CSV, Documentación.
- **Variables de interés:** Tipo; Hora; Municipio; Lesionados/fallecidos según registro; Usuarios involucrados.
- **Llaves propuestas:** ID/llave definida por edición; entidad + municipio + año.
- **CP:** Cruce espacial. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Seguridad vial alrededor de escuelas y conexiones de transporte.
- **Límites:** No asumir cobertura carretera federal ni coordenadas para todos los municipios. Revisar notas por año/municipio antes de comparar tasas.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.
- **Prueba y ejemplos:** [inegi-atus](../source_tests/README.md#inegi-atus).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.inegi.org.mx/programas/accidentes/default.html) — `indexed_primary`. Programa ATUS oficial localizado; georreferenciación desde 2019 sólo para municipios seleccionados.

### Fuentes sorprendentes y multimodales

#### dof-publicaciones

**DOF/SIDOF: publicaciones y reformas para explicar Git** — SEGOB / Diario Oficial de la Federación.

- **Contenido:** mixto; modalidades: text, tabular.
- **Cobertura y unidad:** México. Publicación identificada por código; secciones y documentos.
- **Periodo / actualización:** Archivo histórico; ejemplo publicado 27-12-2022. Ediciones del DOF.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: HTML, PDF, Servicios web documentados.
- **Variables de interés:** Código de nota; Fecha de publicación; Dependencia; Título; Texto y transitorios.
- **Llaves propuestas:** Código de nota + edición/fecha; hash del archivo recuperado.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Versionar una representación didáctica de la reforma de vacaciones; comparar commits y registrar procedencia. Extraer dependencias, temas y artículos reformados para un buscador documental.
- **Límites:** Una reforma se publica como documento nuevo; no sobrescribe automáticamente el texto histórico. Git no consolida leyes: la equivalencia con commits/ramas es pedagógica. Fecha de publicación y entrada en vigor difieren. HTML convertido puede perder elementos; cotejar la edición PDF para uso jurídico.
- **Uso:** Conservar referencia oficial y separar la transformación didáctica del documento publicado.
- **Prueba y ejemplos:** [dof-publicaciones](../source_tests/README.md#dof-publicaciones).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://sidof.segob.gob.mx/datos_abiertos) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://sidof.segob.gob.mx/notas/docFuente/5675889).

#### usgs-sismos

**Terremotos del último día y sus revisiones** — USGS.

- **Contenido:** estructurado; modalidades: tabular, geospatial, time_series.
- **Cobertura y unidad:** Mundial; capacidad de detección desigual. Evento sísmico revisable.
- **Periodo / actualización:** Ventana móvil de 24 horas. Actualizaciones frecuentes.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: GeoJSON.
- **Variables de interés:** Magnitud; Profundidad; Coordenadas; Hora; Estado de revisión.
- **Llaves propuestas:** ID de evento + instante de captura.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Comparar magnitud y profundidad; mostrar cómo se corrige un mismo evento con nueva evidencia.
- **Límites:** La ausencia de eventos no prueba ausencia de sismicidad. Magnitud y ubicación pueden revisarse; no convertir un mapa en predicción sísmica.
- **Uso:** Atribuir a USGS y preservar actualización y estado de revisión.
- **Prueba y ejemplos:** [usgs-sismos](../source_tests/README.md#usgs-sismos).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson).

#### nasa-exoplanetas

**Planetas fuera del Sistema Solar** — NASA Exoplanet Archive / Caltech-IPAC.

- **Contenido:** estructurado; modalidades: tabular.
- **Cobertura y unidad:** Exoplanetas incluidos en el archivo. Planeta; tabla de parámetros compuestos.
- **Periodo / actualización:** Archivo por descubrimiento/publicación; corte de consulta. Actualización del archivo.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: CSV, JSON, VOTable.
- **Variables de interés:** Nombre; Estrella; Método de descubrimiento; Año; Periodo orbital.
- **Llaves propuestas:** Nombre de planeta; tabla/versión de consulta.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** ¿Qué tipos de planetas descubre cada método? Visualizar sesgo de detección y valores faltantes.
- **Límites:** El catálogo observado no es una muestra uniforme de todos los planetas. Revisar unidades e incertidumbres antes de comparar masa/radio.
- **Uso:** Citar NASA Exoplanet Archive, la tabla y referencias científicas de cada medición.
- **Prueba y ejemplos:** [nasa-exoplanetas](../source_tests/README.md#nasa-exoplanetas).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+top+3+pl_name,hostname,discoverymethod,disc_year,pl_orbper+from+pscomppars&format=csv).

#### gwosc-ondas-gravitacionales

**Colisiones de agujeros negros y ondas gravitacionales** — LIGO/Virgo/KAGRA / GWOSC.

- **Contenido:** mixto; modalidades: tabular, time_series.
- **Cobertura y unidad:** Detecciones incluidas en catálogos de colaboración. Evento y versión de estimación; catálogo en la muestra inicial.
- **Periodo / actualización:** Catálogos publicados. Por publicación/revisión.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: JSON, HDF5, FITS.
- **Variables de interés:** Nombre de evento; Catálogo; Masas estimadas; Distancia; Señal temporal.
- **Llaves propuestas:** Evento + catálogo + versión.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Explorar masas y distancias; pasar de una señal ruidosa a una detección.
- **Límites:** La muestra de catálogos no contiene por sí sola las señales ni prueba su descarga. Parámetros son estimaciones con incertidumbre, no mediciones exactas.
- **Uso:** Usar la política de atribución y DOI de cada catálogo/dataset.
- **Prueba y ejemplos:** [gwosc-ondas-gravitacionales](../source_tests/README.md#gwosc-ondas-gravitacionales).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://gwosc.org/api/) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://gwosc.org/api/v2/catalogs?format=json).

#### noaa-ghcn

**El clima escrito por estaciones meteorológicas** — NOAA / NCEI.

- **Contenido:** estructurado; modalidades: tabular, time_series, geospatial.
- **Cobertura y unidad:** Estaciones mundiales con periodos y cobertura desiguales. Estación–fecha–elemento; muestra inicial del catálogo de estaciones.
- **Periodo / actualización:** Histórico variable por estación. Actualización del productor.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: Ancho fijo TXT/DLY, CSV comprimido.
- **Variables de interés:** ID estación; Latitud/longitud; Elevación; Temperatura; Precipitación; Banderas de calidad.
- **Llaves propuestas:** ID de estación + fecha + elemento.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Detectar olas de calor y distinguir clima de ruido por cambio de estación.
- **Límites:** La muestra del catálogo no es una muestra de observaciones meteorológicas. Interpretar -9999, banderas y escalas; una décima de grado no equivale a un grado.
- **Uso:** Citar NOAA/NCEI y documentar filtros de calidad.
- **Prueba y ejemplos:** [noaa-ghcn](../source_tests/README.md#noaa-ghcn).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.ncei.noaa.gov/pub/data/ghcn/daily/) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt).

#### gbif-biodiversidad

**Dónde se ha observado vida: especies y sesgo de muestreo** — GBIF y publicadores de ocurrencias.

- **Contenido:** mixto; modalidades: tabular, geospatial, image.
- **Cobertura y unidad:** Mundial; muestra acotada a México. Registro de ocurrencia de un organismo.
- **Periodo / actualización:** Fechas variables del evento y publicación. Continuo según publicadores.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: JSON, Darwin Core Archive, Multimedia enlazada.
- **Variables de interés:** Taxón; Fecha; Tipo de registro; Localidad; Licencia; Referencias multimedia.
- **Llaves propuestas:** Occurrence key; datasetKey + occurrenceID cuando aplique.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Mapas de biodiversidad y contraste entre riqueza observada y esfuerzo de recolección.
- **Límites:** No confundir ausencia de registros con ausencia de especie. Fotografías y registros tienen licencias propias; coordenadas pueden estar generalizadas.
- **Uso:** Respetar licencia por registro/publicador; descargas formales generan DOI.
- **Prueba y ejemplos:** [gbif-biodiversidad](../source_tests/README.md#gbif-biodiversidad).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://techdocs.gbif.org/en/openapi/v1/occurrence) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://api.gbif.org/v1/occurrence/search?country=MX&limit=3).

#### xeno-canto-audio

**Cantos de aves, murciélagos e insectos** — Xeno-canto y autores de grabaciones.

- **Contenido:** mixto; modalidades: tabular, audio, image.
- **Cobertura y unidad:** Mundial; muestra de la consulta demo documentada. Grabación y metadatos.
- **Periodo / actualización:** Fechas de grabación y carga. Carga comunitaria.
- **Acceso y formatos:** API v3 con clave de cuenta; se prueba únicamente la clave pública demo documentada, sin solicitar credenciales personales. Formatos: JSON, Audio, Sonogramas.
- **Variables de interés:** Especie; Lugar; Fecha; Duración; Tipo de vocalización; Calidad; Enlace de audio.
- **Llaves propuestas:** ID XC de grabación.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Clasificar vocalizaciones y comparar dominios geográficos; enseñar espectrogramas.
- **Límites:** API v3 requiere clave; demo es un ejemplo público del productor y puede limitar consultas. Abrir metadatos no valida descarga ni reproducción del audio. Evitar que grabaciones del mismo individuo/sitio filtren información entre train/test.
- **Uso:** Licencia Creative Commons por grabación; no asumir autorización comercial para todas.
- **Prueba y ejemplos:** [xeno-canto-audio](../source_tests/README.md#xeno-canto-audio).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://xeno-canto.org/explore/api) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://xeno-canto.org/api/3/recordings?query=gen:larus+sp:fuscus&key=demo&per_page=2).

#### met-arte

**Arte, objetos e imágenes del Metropolitan Museum** — The Metropolitan Museum of Art.

- **Contenido:** mixto; modalidades: tabular, text, image.
- **Cobertura y unidad:** Colección del museo. Objeto y sus imágenes/metadatos.
- **Periodo / actualización:** Fechas históricas de las obras y corte del catálogo. Actualizaciones del catálogo.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: JSON, CSV, Imágenes.
- **Variables de interés:** Título; Artista; Fecha; Material; Departamento; isPublicDomain; Imagen.
- **Llaves propuestas:** objectID; identificadores de artista cuando existan.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Explorar materiales, periodos y representaciones; búsqueda por texto e imagen.
- **Límites:** Una colección museística tiene sesgos de adquisición y catalogación. Validar isPublicDomain y derechos antes de descargar/republicar imágenes.
- **Uso:** Usar las condiciones Open Access del museo y el estado de derechos de cada obra.
- **Prueba y ejemplos:** [met-arte](../source_tests/README.md#met-arte).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://metmuseum.github.io/) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://collectionapi.metmuseum.org/public/collection/v1/objects/436535).

#### loc-prensa-historica

**Periódicos antiguos: portadas, OCR y metadatos** — Library of Congress / Chronicling America.

- **Contenido:** mixto; modalidades: tabular, text, image.
- **Cobertura y unidad:** Colecciones disponibles en la Library of Congress. Título/ejemplar/página; distinguir niveles.
- **Periodo / actualización:** Periódicos históricos según colección. Digitalización y actualización del catálogo.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: JSON, OCR, JPEG/TIFF, IIIF.
- **Variables de interés:** Título; Fecha; Idioma; Lugar; Páginas; Enlaces a recursos.
- **Llaves propuestas:** Item ID + resource/page ID.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Rastrear vocabulario de epidemias o tecnología a través de décadas y revisar errores OCR.
- **Límites:** Una búsqueda de títulos no equivale a recuperar páginas ni OCR. Digitalización selectiva y errores de reconocimiento sesgan frecuencias.
- **Uso:** Revisar Rights & Access del ítem; no todas las colecciones tienen las mismas condiciones.
- **Prueba y ejemplos:** [loc-prensa-historica](../source_tests/README.md#loc-prensa-historica).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.loc.gov/apis/json-and-yaml/) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://www.loc.gov/newspapers/?fo=json&c=3).

#### gutenberg-quijote

**Don Quijote como corpus de lenguaje** — Project Gutenberg / Miguel de Cervantes.

- **Contenido:** no_estructurado; modalidades: text.
- **Cobertura y unidad:** Obra en español de dos partes. Libro, capítulo y segmento de texto.
- **Periodo / actualización:** 1605/1615; edición digital del productor. Correcciones de edición digital.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: TXT, HTML, EPUB.
- **Variables de interés:** Texto; Capítulos; Diálogos; Metadatos de edición.
- **Llaves propuestas:** eBook ID + edición/hash + capítulo/offset.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Redes de personajes, cambio de vocabulario y búsqueda semántica reproducible.
- **Límites:** Separar encabezados/licencia del contenido literario. Una edición no representa por sí sola el español de una época; documentar normalización.
- **Uso:** Revisar licencia Project Gutenberg y condición de dominio público en la jurisdicción de uso.
- **Prueba y ejemplos:** [gutenberg-quijote](../source_tests/README.md#gutenberg-quijote).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.gutenberg.org/ebooks/2000) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://www.gutenberg.org/cache/epub/2000/pg2000.txt).

#### openfoodfacts-alimentos

**Alimentos: ingredientes, nutrientes y fotos de etiquetas** — Open Food Facts y contribuyentes.

- **Contenido:** mixto; modalidades: tabular, text, image.
- **Cobertura y unidad:** Mundial; cobertura comunitaria. Producto por código de barras y versión.
- **Periodo / actualización:** Última edición de cada producto. Actualización colaborativa.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: JSON, CSV/JSONL, Imágenes.
- **Variables de interés:** Código de barras; Ingredientes; Nutrientes; Marca; Etiquetas; Imagen.
- **Llaves propuestas:** Barcode como texto + fecha de edición.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Detectar ingredientes o comparar azúcar por 100 g; contrastar etiqueta con datos capturados.
- **Límites:** No inferir calidad de dieta individual de un producto aislado. Revisar unidades, nutrientes faltantes, reformulaciones y país de comercialización.
- **Uso:** Base ODbL; revisar también atribución y licencia de imágenes/textos del productor.
- **Prueba y ejemplos:** [openfoodfacts-alimentos](../source_tests/README.md#openfoodfacts-alimentos).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://world.openfoodfacts.org/api/v2/product/3017620422003?fields=code,product_name,brands,nutriments,nutriscore_grade,image_url).

#### nuforc-ovnis

**Relatos de avistamientos de ovnis/UAP** — National UFO Reporting Center.

- **Contenido:** mixto; modalidades: tabular, text, image.
- **Cobertura y unidad:** Reportes enviados al centro; cobertura desigual. Reporte narrativo y clasificación.
- **Periodo / actualización:** Fecha declarada del evento y de publicación. Publicaciones del productor.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: HTML, Texto, Multimedia cuando exista.
- **Variables de interés:** Fecha declarada; Lugar; Forma reportada; Duración; Relato; Clasificación del centro.
- **Llaves propuestas:** ID de reporte + fecha de captura.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Analizar patrones del lenguaje y efectos de cobertura mediática en reportes.
- **Límites:** Son reportes/autopercepciones; no evidencia de visitas extraterrestres. No hay descarga masiva/API abierta validada; no confundir portal accesible con permiso de scraping ilimitado.
- **Uso:** Consultar condiciones del productor; conservar sólo ejemplos breves y enlaces hasta verificar redistribución.
- **Prueba y ejemplos:** [nuforc-ovnis](../source_tests/README.md#nuforc-ovnis).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://nuforc.org/databank/) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://nuforc.org/databank/?id=latest).

#### gdelt-noticias

**El mundo contado por noticias: eventos y menciones** — The GDELT Project.

- **Contenido:** mixto; modalidades: tabular, text, geospatial.
- **Cobertura y unidad:** Cobertura mediática mundial, desigual por idioma/medio. Evento codificado, mención o registro GKG; archivos separados.
- **Periodo / actualización:** GDELT 2.0; lotes recientes de 15 minutos. Cada 15 minutos en GDELT 2.0.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: TSV/ZIP, TXT índice, URLs de noticias.
- **Variables de interés:** Actores; Código de evento; Fecha; Geografía; Tono; URL de fuente.
- **Llaves propuestas:** GlobalEventID en Events; llaves propias en Mentions/GKG.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Comparar narrativas y sesgos de cobertura entre regiones, sin equiparar noticia con hecho verificado.
- **Límites:** La muestra lastupdate es un manifiesto de archivos, no un conjunto de eventos. El texto completo de artículos no viene necesariamente en el dataset y mantiene derechos del editor.
- **Uso:** Atribuir GDELT y respetar las condiciones de las noticias enlazadas.
- **Prueba y ejemplos:** [gdelt-noticias](../source_tests/README.md#gdelt-noticias).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://www.gdeltproject.org/data.html) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://data.gdeltproject.org/gdeltv2/lastupdate.txt).

#### nasa-bolidos

**Bólidos: entradas atmosféricas detectadas por sensores** — NASA / JPL / CNEOS.

- **Contenido:** estructurado; modalidades: tabular, geospatial, time_series.
- **Cobertura y unidad:** Eventos detectados y publicados, cobertura instrumental no uniforme. Evento de bólido.
- **Periodo / actualización:** Catálogo de eventos; corte de consulta. Actualización del productor.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: JSON.
- **Variables de interés:** Fecha UTC; Energía; Coordenadas; Altitud; Velocidad.
- **Llaves propuestas:** Fecha + referencia de catálogo; revisar ausencia de ID único.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** Relación entre energía y altitud; detectar datos faltantes y errores al interpretar hemisferios.
- **Límites:** No es un censo completo de meteoritos; bólido no implica material recuperado. No hay coordenadas o velocidad para todos los registros; respetar unidades y versión API.
- **Uso:** Atribuir NASA/JPL/CNEOS y respetar Fair Use del servicio.
- **Prueba y ejemplos:** [nasa-bolidos](../source_tests/README.md#nasa-bolidos).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://ssd-api.jpl.nasa.gov/doc/fireball.html) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://ssd-api.jpl.nasa.gov/fireball.api?limit=3).

#### nyc-ratas

**Inspecciones de ratas por predio en Nueva York** — NYC DOHMH / NYC Open Data.

- **Contenido:** mixto; modalidades: tabular, text, geospatial.
- **Cobertura y unidad:** Nueva York; predios inspeccionados. Inspección/intervención en predio.
- **Periodo / actualización:** Archivo con fechas de inspección; corte de consulta. Diaria según ficha.
- **Acceso y formatos:** Consulta pública acotada; confirmar el resultado de acceso en source_tests/README.md. Formatos: JSON, CSV, GeoJSON.
- **Variables de interés:** Tipo de inspección; Fecha; Resultado; Borough; ZIP code; Observaciones.
- **Llaves propuestas:** Llave administrativa + tipo/fecha según diccionario; BBL enlaza predios.
- **CP:** Campo documentado. **Prioridad:** P2. **Esfuerzo:** Media.
- **Integración:** `not_ingested`.
- **Análisis:** ¿Hay más ratas o más inspecciones? Mostrar denominadores y sesgo de vigilancia.
- **Límites:** No inspeccionado no equivale a libre de ratas. ZIP de EE. UU. no es un CP mexicano; el conteo de inspecciones no estima población de roedores.
- **Uso:** Usar términos NYC Open Data y las notas de limitación de DOHMH.
- **Prueba y ejemplos:** [nyc-ratas](../source_tests/README.md#nyc-ratas).

**Fuentes y antecedente de verificación:**

- [Fuente 1](https://data.cityofnewyork.us/Health/Rodent-Inspection/p937-wjvj/about_data) — `primary_documentation_located`. Fuente del productor localizada; el resultado de la prueba HTTP está separado en source_tests/results.json. [Recurso localizado](https://data.cityofnewyork.us/resource/p937-wjvj.json?$limit=3).

## Incorporación posterior y mantenimiento

Antes de incorporar una fuente a los recolectores: probar un archivo, identificar corte/licencia, guardar diccionario, comprobar llaves/cobertura y definir el histórico necesario. No añadir a `configs/tables.yml` hasta disponer de una extracción reproducible. La recolección de movilidad existente conserva su configuración.

Para actualizar este catálogo, mantener alineados `catalogs/datasets_reales_mexico.json`, este documento y `catalogs/source_probes.json`. Las pruebas producen juntas `source_tests/README.md` y `source_tests/results.json`; las rutas y archivos cambian, por lo que el resultado es fechado y no una garantía permanente.
