# Catálogo de datasets reales para analizar en México

Revisión: **4 de noviembre de 2026**, zona `America/Mexico_City`. Repositorio: `jcval94/DataCollectionMov`.

30 fichas de datasets, productos y fuentes documentales reales. La selección prioriza preguntas sobre oportunidades educativas, movilidad, desigualdad territorial y uso de recursos públicos. Incluye fuentes del sorteo alusivo al avión presidencial.

**Alcance:** catálogo con enlaces y propuestas; las nuevas fuentes todavía no están ingeridas. Sólo se identifican como existentes las integraciones comprobadas en el código y el árbol del repo. Esta revisión no ejecutó APIs autenticadas ni descargas masivas y no evalúa la salud de los workflows.

- [Versión estructurada JSON](../catalogs/datasets_reales_mexico.json): mismos 30 registros, fuentes, acceso, periodicidad, variables, llaves de cruce y limitaciones.
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

## Índice

| ID | Fuente o producto | Prioridad / esfuerzo | Relación con CP | Estado en el repo |
| --- | --- | --- | --- |
| [rifa-235-premios](#rifa-235-premios) | GSE 235: lista oficial de premios | P2 / Alta | No asumir | Por incorporar |
| [rifa-235-reportes](#rifa-235-reportes) | GSE 235: balance y beneficiarios publicados | P2 / Media | No asumir | Por incorporar |
| [rifa-235-asf](#rifa-235-asf) | GSE 235: auditoría de gestión financiera | P1 / Media | No asumir | Por incorporar |
| [inegi-indicadores-api](#inegi-indicadores-api) | API del Banco de Indicadores | P1 / Baja | No asumir | Por incorporar |
| [inegi-denue](#inegi-denue) | DENUE: establecimientos y actividad económica | P1 / Baja | Sí, documentado | Integración parcial |
| [inegi-censo-2020-ageb](#inegi-censo-2020-ageb) | Censo 2020: indicadores por AGEB y manzana urbana | P1 / Media | Cruce espacial | Por incorporar |
| [inegi-marco-geoestadistico](#inegi-marco-geoestadistico) | Marco Geoestadístico y equivalencias | P1 / Media | Cruce espacial | Por incorporar |
| [inegi-entorno-urbano-2020](#inegi-entorno-urbano-2020) | Características del entorno urbano 2020 | P2 / Media | Cruce espacial | Por incorporar |
| [inegi-enigh-2024](#inegi-enigh-2024) | ENIGH 2024: ingresos y gastos del hogar | P1 / Media | No asumir | Por incorporar |
| [inegi-enoe](#inegi-enoe) | ENOE: empleo, ingresos laborales e informalidad | P2 / Media | No asumir | Por incorporar |
| [inegi-eod-zmvm-2017](#inegi-eod-zmvm-2017) | Encuesta Origen Destino ZMVM 2017 | P1 / Media | No asumir | Por incorporar |
| [sepomex-codigos-postales](#sepomex-codigos-postales) | Catálogo Nacional de Códigos Postales | P1 / Baja | Catálogo postal | Por incorporar |
| [cdmx-codigos-postales-poligonos](#cdmx-codigos-postales-poligonos) | Códigos postales CDMX: capa geográfica | P1 / Baja | Polígonos CP | Por incorporar |
| [shcp-pef](#shcp-pef) | Presupuesto de Egresos de la Federación aprobado | P1 / Media | No asumir | Por incorporar |
| [shcp-cuenta-publica](#shcp-cuenta-publica) | Cuenta Pública: gasto al cierre | P1 / Media | No asumir | Por incorporar |
| [shcp-srft](#shcp-srft) | SRFT: ejercicio y destino del gasto federalizado | P1 / Alta | Cruce espacial | Por incorporar |
| [sep-cct](#sep-cct) | Catálogo de Centros de Trabajo | P1 / Media | Por confirmar | Por incorporar |
| [sep-formato-911](#sep-formato-911) | Formato 911: alumnado, docentes y escuelas | P1 / Media | Por confirmar | Por incorporar |
| [anuies-anuario](#anuies-anuario) | Anuario Estadístico de Educación Superior | P2 / Media | No asumir | Por incorporar |
| [ceey-emovi-2023](#ceey-emovi-2023) | ESRU–EMOVI 2023 | P1 / Media | No asumir | Por incorporar |
| [ceey-emovi-2017](#ceey-emovi-2017) | ESRU–EMOVI 2017 | P1 / Media | No asumir | Por incorporar |
| [inegi-mmsi-2016](#inegi-mmsi-2016) | Módulo de Movilidad Social Intergeneracional 2016 | P2 / Media | No asumir | Por incorporar |
| [coneval-pobreza-municipal](#coneval-pobreza-municipal) | Pobreza municipal 2010–2020 | P1 / Baja | No asumir | Por incorporar |
| [conapo-marginacion-2020](#conapo-marginacion-2020) | Índices de marginación 2020 | P1 / Baja | Cruce espacial | Por incorporar |
| [metrobus-gtfs](#metrobus-gtfs) | Metrobús: GTFS estático y tiempo real | P1 / Baja | Cruce espacial | Implementado; current localizado |
| [ecobici-viajes](#ecobici-viajes) | ECOBICI: viajes históricos | P1 / Baja | Cruce espacial | Recolector; current objetivo no localizado |
| [ecobici-gbfs](#ecobici-gbfs) | ECOBICI: catálogo y disponibilidad GBFS | P2 / Baja | Cruce espacial | Implementado; current localizado |
| [salud-clues](#salud-clues) | CLUES: establecimientos de salud | P1 / Baja | Sí, documentado | Por incorporar |
| [cdmx-fgj-carpetas](#cdmx-fgj-carpetas) | Carpetas de investigación FGJ CDMX | P2 / Media | Cruce espacial | Por incorporar |
| [inegi-atus](#inegi-atus) | ATUS: accidentes de tránsito urbanos y suburbanos | P2 / Media | Cruce espacial | Por incorporar |

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

- **Cobertura y unidad:** México. Billete premiado.
- **Periodo / actualización:** 15-09-2020. Evento único.
- **Acceso y formatos:** Recuperar PDF histórico citado; requiere extracción y revisión manual. Formatos: PDF.
- **Variables de interés:** Número de billete; Premio; Número y fecha de sorteo.
- **Llaves para cruzar:** sorteo + número de billete (texto, conservar longitud).
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Alta.
- **Estado:** Por incorporar.
- **Análisis:** Distribución de números ganadores y simulación del sorteo.
- **Límites:** PDF no recuperado en esta revisión; no existe CSV validado en el repo. Lista de ganadores no equivale a registro de ventas ni de cobro; no permite atribuir irregularidades.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://www.gob.mx/lotenal/prensa/con-gran-apoyo-de-la-sociedad-lotenal-llevo-a-cabo-con-exito-el-gran-sorteo-especial-no-235?idiom=es-MX) — Fuente indexada; apertura fallida. Comunicado oficial indexado; apertura devolvió 403. Cita la lista en http://www.lotenal.gob.mx/Comercial/Listas/235.pdf; la variante HTTPS no pudo recuperarse. [Archivo o recurso localizado](http://www.lotenal.gob.mx/Comercial/Listas/235.pdf).

#### rifa-235-reportes

**GSE 235: balance y beneficiarios publicados** — Lotería Nacional / INDEP.

- **Cobertura y unidad:** México; instituciones mencionadas. Concepto financiero o institución, separado por documento.
- **Periodo / actualización:** Comunicados de 2020. Evento único; reportes con diferentes cortes.
- **Acceso y formatos:** Reconstrucción documental; no hay microdatos completos de ventas verificados. Formatos: HTML.
- **Variables de interés:** Ventas; Premios; Gastos; Remanente; Instituciones reportadas.
- **Llaves para cruzar:** documento + fecha de publicación + concepto; CCT/CLUES sólo tras correspondencia documentada.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Comparar balances por fecha; documentar escuelas beneficiarias.
- **Límites:** Separar cortes y definiciones: las cifras iniciales y auditadas pueden diferir. Una escuela mencionada no trae necesariamente CCT; vincular sólo con evidencia.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://www.gob.mx/lotenal/prensa/197193) — Fuente indexada; apertura fallida. Comunicado del 11-12-2020 indexado; apertura devolvió 403.
- [Fuente 2](https://www.gob.mx/indep/prensa/informa-indep-que-siete-escuelas-recibieron-premios-del-sorteo-alusivo-al-avion-presidencial) — Fuente primaria indexada. Comunicado oficial localizado en el índice de búsqueda; archivo tabular no comprobado.

#### rifa-235-asf

**GSE 235: auditoría de gestión financiera** — Auditoría Superior de la Federación.

- **Cobertura y unidad:** México. Concepto o categoría del resultado 4.
- **Periodo / actualización:** Cuenta Pública 2020; revisión posterior. Informe histórico.
- **Acceso y formatos:** PDF público legible; extraer tablas de las páginas impresas 23–31. Formatos: PDF.
- **Variables de interés:** Billetes vendidos y no vendidos; Tipo de ganador; Premios pagados; Flujos y rentabilidad.
- **Llaves para cruzar:** auditoría + página + concepto + unidad.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Conciliar ventas, premios y remanentes contra los comunicados.
- **Límites:** El PDF contiene discrepancias internas: conservar página, unidad y literal original. Importes expresados en miles de pesos; distinguirlos de pesos.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://www.asf.gob.mx/Trans/Informes/IR2020c/Documentos/Auditorias/2020_0051_a.pdf) — Contenido primario leído. PDF legible de 68 páginas; resultado 4, páginas impresas 23–31, dedicado al GSE 235. [Archivo o recurso localizado](https://www.asf.gob.mx/Trans/Informes/IR2020c/Documentos/Auditorias/2020_0051_a.pdf).

### INEGI y contexto

#### inegi-indicadores-api

**API del Banco de Indicadores** — INEGI.

- **Cobertura y unidad:** México; geografía disponible según indicador. Indicador × área × periodo.
- **Periodo / actualización:** Series variables según indicador. Según indicador.
- **Acceso y formatos:** API con token INEGI; seleccionar IDs mediante catálogo de metadatos. Formatos: JSON, XML.
- **Variables de interés:** ID de indicador; Periodo; Valor; Unidad; Área geográfica.
- **Llaves para cruzar:** ID indicador + área + periodo + fuente/versión.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Estado:** Por incorporar.
- **Análisis:** Series de población, precios o actividad para contextualizar transporte y gasto.
- **Límites:** No todos los indicadores admiten municipio o AGEB. Guardar unidad, base, frecuencia, fuente y revisiones; no asumir que el token DENUE sirve sin comprobar.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.

**Fuentes y verificación:**

- [Fuente 1](https://www.inegi.org.mx/servicios/api-indicadores/) — Contenido primario leído. Documentación de indicadores y catálogo de metadatos leída. No se ejecutaron consultas con token.

#### inegi-denue

**DENUE: establecimientos y actividad económica** — INEGI.

- **Cobertura y unidad:** Nacional; extracción actual centrada en educación CDMX. Establecimiento por edición/snapshot.
- **Periodo / actualización:** Edición vigente y snapshots propios. Ediciones del productor; consulta mensual en este repo.
- **Acceso y formatos:** API con token; ampliar sectores o estados cuando se implemente. Formatos: JSON API, Descarga masiva.
- **Variables de interés:** CLEE/ID; Actividad SCIAN; Estrato de personal; CP; Latitud y longitud.
- **Llaves para cruzar:** CLEE o ID establecimiento + edición; CP como agrupación; coordenadas para cruce espacial.
- **CP:** Sí, documentado. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Estado:** Integración parcial. Rutas: [`src/historico_api/sources/denue.py`](../src/historico_api/sources/denue.py), [`data/current/denue_cdmx_sector_61_servicios_educativos.csv`](../data/current/denue_cdmx_sector_61_servicios_educativos.csv).
- **Análisis:** Mapear servicios y concentración de escuelas por CP y acceso al Metrobús.
- **Límites:** Estrato de personal no es facturación ni empleo exacto. La integración actual no cubre todo DENUE; usar ID/CLEE y edición al deduplicar.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.

**Fuentes y verificación:**

- [Fuente 1](https://www.inegi.org.mx/servicios/api-denue/) — Fuente indexada; apertura fallida. Documentación oficial indexada con campo CP; apertura devolvió 502. Integración y campo cp confirmados en el código del repo.

#### inegi-censo-2020-ageb

**Censo 2020: indicadores por AGEB y manzana urbana** — INEGI.

- **Cobertura y unidad:** México; resultados urbanos a pequeña área. Área geográfica × indicador; separar agregados.
- **Periodo / actualización:** 2020. Censal; puede haber correcciones del archivo.
- **Acceso y formatos:** Descarga desde programa CPV 2020; seleccionar resultados AGEB/manzana urbana. Formatos: CSV/ZIP, Diccionario.
- **Variables de interés:** Población; Edad; Escolaridad; Discapacidad; Vivienda.
- **Llaves para cruzar:** Entidad (2) + municipio (3) + localidad (4) + AGEB (4); manzana (3) cuando proceda.
- **CP:** Cruce espacial. **Prioridad:** P1. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Estimar población y rezago educativo cerca de estaciones y escuelas.
- **Límites:** CP no es AGEB; manejar asteriscos y valores reservados como faltantes. No sumar filas totales con manzanas; mantener claves geográficas como texto.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.

**Fuentes y verificación:**

- [Fuente 1](https://www.inegi.org.mx/programas/ccpv/2020/) — Fuente primaria indexada. Programa oficial y disponibilidad de resultados por AGEB/manzana localizados. La ficha antigua tit=326085 devolvió 'archivo no existe'; usar el programa como entrada.

#### inegi-marco-geoestadistico

**Marco Geoestadístico y equivalencias** — INEGI.

- **Cobertura y unidad:** Nacional. Polígono, localidad o clave por edición.
- **Periodo / actualización:** Edición compatible con el dato analizado; 2020 para Censo 2020. Actualizaciones por edición.
- **Acceso y formatos:** Descargar edición y entidad desde portal oficial. Formatos: SHP/ZIP, Catálogos.
- **Variables de interés:** CVEGEO; Entidad; Municipio; Localidad; AGEB; Geometría.
- **Llaves para cruzar:** CVEGEO + edición + nivel.
- **CP:** Cruce espacial. **Prioridad:** P1. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Unir censo con estaciones, escuelas, CP y presupuesto territorial.
- **Límites:** Fijar edición y CRS; cambios de límites requieren equivalencias. Geografía estadística no equivale automáticamente a límite jurídico.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.

**Fuentes y verificación:**

- [Fuente 1](https://www.inegi.org.mx/temas/mg/) — Fuente primaria indexada. Portal oficial de descargas y metadatos del Marco Geoestadístico localizados.

#### inegi-entorno-urbano-2020

**Características del entorno urbano 2020** — INEGI.

- **Cobertura y unidad:** Localidades urbanas cubiertas por el levantamiento. Manzana y vialidad, tablas distintas.
- **Periodo / actualización:** 2020. Levantamiento 2020.
- **Acceso y formatos:** Microdatos del CPV 2020 enlazados en metadatos oficiales. Formatos: Bases descargables, Diccionario XLSX.
- **Variables de interés:** Banquetas; Rampas; Alumbrado; Características viales.
- **Llaves para cruzar:** Clave geográfica de manzana/vialidad según diccionario + edición.
- **CP:** Cruce espacial. **Prioridad:** P2. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Accesibilidad peatonal en el entorno de escuelas y estaciones.
- **Límites:** Revisar categorías y cobertura exacta de cada variable. Infraestructura registrada en 2020 no describe necesariamente el estado actual.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.

**Fuentes y verificación:**

- [Fuente 1](https://www.inegi.org.mx/rnm/index.php/catalog/941/related-materials) — Fuente primaria indexada. Metadatos oficiales identifican tablas de Vialidad y Manzana y enlazan los microdatos del CPV 2020.

#### inegi-enigh-2024

**ENIGH 2024: ingresos y gastos del hogar** — INEGI.

- **Cobertura y unidad:** Nacional y dominios de estimación de la encuesta. Vivienda, hogar, persona, ingreso o gasto; tablas relacionadas.
- **Periodo / actualización:** 2024; ediciones anteriores en el programa. Bienal.
- **Acceso y formatos:** Microdatos públicos por edición. Formatos: CSV/ZIP, Documentación.
- **Variables de interés:** Ingreso corriente; Gasto en transporte; Gasto educativo; Composición del hogar.
- **Llaves para cruzar:** folioviv + foliohog; numren en tablas de personas, según diccionario; Entidad para agregados representativos.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Carga del transporte y educación sobre el ingreso, por decil y entidad.
- **Límites:** Usar ponderadores, estratos y UPM; no estimar por CP o manzana. Es corte transversal: no mide por sí sola movilidad intergeneracional.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.

**Fuentes y verificación:**

- [Fuente 1](https://www.inegi.org.mx/programas/enigh/nc/2024/) — Fuente primaria indexada. Programa oficial, microdatos y documentación ENIGH 2024 localizados.

#### inegi-enoe

**ENOE: empleo, ingresos laborales e informalidad** — INEGI.

- **Cobertura y unidad:** Nacional, entidades y ciudades autorrepresentadas según edición. Persona y hogar por trimestre.
- **Periodo / actualización:** Desde 2005; seleccionar trimestre disponible. Indicadores mensuales y trimestrales; microdatos por corte.
- **Acceso y formatos:** Microdatos públicos; fijar periodo y versión. Formatos: CSV/DBF según edición, Documentación.
- **Variables de interés:** Escolaridad; Ocupación; Horas; Ingreso laboral; Informalidad.
- **Llaves para cruzar:** Llaves de vivienda/hogar/persona y trimestre según diccionario.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Brechas laborales por escolaridad, edad y género.
- **Límites:** Diseño muestral y cambios durante pandemia requieren tratamiento. No unir personas entre encuestas distintas; no inferir salarios por CP.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.

**Fuentes y verificación:**

- [Fuente 1](https://www.inegi.org.mx/programas/enoe/15ymas/) — Fuente primaria indexada. Programa oficial y notas sobre revisiones de microdatos localizados; no se determinó el último trimestre descargable.

#### inegi-eod-zmvm-2017

**Encuesta Origen Destino ZMVM 2017** — INEGI / gobiernos CDMX y Estado de México.

- **Cobertura y unidad:** ZMVM dentro de la cobertura de la encuesta. Hogar, persona y viaje.
- **Periodo / actualización:** 2017. Levantamiento específico.
- **Acceso y formatos:** Descarga por programa; revisar distritos y factores. Formatos: Microdatos, Tabulados, Cartografía/documentación.
- **Variables de interés:** Origen/destino; Motivo; Modo; Tiempo; Costo.
- **Llaves para cruzar:** Identificadores de hogar/persona/viaje y distrito según diccionario.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Viajes a estudiar; carga de traslado y conexiones con transporte público.
- **Límites:** Distritos EOD no son CP; revisar cartografía y dominios. La red y los patrones de 2017 son una referencia histórica.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.

**Fuentes y verificación:**

- [Fuente 1](https://www.inegi.org.mx/programas/eod/2017/default.html) — Fuente primaria indexada. Programa oficial de la EOD ZMVM 2017 y catálogo de microdatos localizados.

### Código postal y territorio

#### sepomex-codigos-postales

**Catálogo Nacional de Códigos Postales** — Servicio Postal Mexicano.

- **Cobertura y unidad:** México. Asentamiento × CP; un CP puede tener varios asentamientos.
- **Periodo / actualización:** Corte del archivo descargado. Actualización del productor, sin calendario validado.
- **Acceso y formatos:** Exportación por entidad o país en formulario; descarga no probada. Formatos: TXT, Excel/XML según formulario.
- **Variables de interés:** CP; Asentamiento; Tipo de asentamiento; Municipio; Entidad.
- **Llaves para cruzar:** CP + identificador de asentamiento; validar unicidad; Claves de entidad/municipio previa homologación.
- **CP:** Catálogo postal. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Estado:** Por incorporar.
- **Análisis:** Normalizar domicilios y explorar desigualdad de servicios por CP.
- **Límites:** Conservar CP como texto de cinco dígitos, incluidos ceros iniciales. No ofrece por sí solo polígonos ni relación uno a uno CP–municipio.
- **Uso:** La consulta oficial indica gratuidad y prohíbe comercialización total o parcial del catálogo; revisar aviso antes de redistribuir.

**Fuentes y verificación:**

- [Fuente 1](https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx) — Fuente indexada; apertura fallida. Página oficial de exportación localizada; apertura agotó el tiempo. El formulario y sus descargas no se probaron.

#### cdmx-codigos-postales-poligonos

**Códigos postales CDMX: capa geográfica** — Gobierno de la Ciudad de México.

- **Cobertura y unidad:** Ciudad de México. Polígono de código postal.
- **Periodo / actualización:** Edición del recurso; no determinada en esta revisión. Sin calendario validado.
- **Acceso y formatos:** Recurso geográfico desde ficha CKAN; descarga pendiente. Formatos: GeoJSON.
- **Variables de interés:** Código postal; Geometría.
- **Llaves para cruzar:** CP (texto); unión espacial punto–polígono.
- **CP:** Polígonos CP. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Estado:** Por incorporar.
- **Análisis:** Asignar CP a establecimientos, estaciones y unidades de salud por coordenadas.
- **Límites:** Revisar CRS, geometrías, solapes y fecha de corte. Un polígono CP no reproduce una AGEB; no agregar población sin regla espacial explícita.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://www.datos.cdmx.gob.mx/es_AR/dataset/codigos-postales) — Fuente primaria indexada. Ficha oficial indexada anuncia GeoJSON. La variante /dataset/codigos-postales agotó el tiempo; geometrías no descargadas.

### Presupuesto

#### shcp-pef

**Presupuesto de Egresos de la Federación aprobado** — SHCP.

- **Cobertura y unidad:** Federal; entidad cuando el registro la desagrega. Clave presupuestaria × ejercicio.
- **Periodo / actualización:** PEF 2026 identificado; otros ejercicios según portal. Anual.
- **Acceso y formatos:** Ficha y analíticos oficiales; descarga bloqueada durante esta revisión. Formatos: Bases tabulares, Catálogos, Analíticos.
- **Variables de interés:** Ramo; Unidad responsable; Programa; Objeto/tipo de gasto; Monto aprobado.
- **Llaves para cruzar:** Ejercicio + clave presupuestaria completa del recurso.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Asignación a educación, salud y movilidad por programa y habitante.
- **Límites:** PPEF es propuesta; PEF es aprobado: nunca intercambiarlos. Ubicación presupuestaria puede ser unidad ejecutora y no beneficiarios; homogeneizar pesos reales.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://www.datos.gob.mx/dataset/presupuesto_egresos_federacion_pef) — Fuente indexada; apertura fallida. Ficha oficial indexada describe el PEF 2026; apertura devolvió 403. El portal de analíticos devolvió 502.
- [Fuente 2](https://www.pef.hacienda.gob.mx/es/PEF/Analiticos_PresupuestariosPEF) — Fuente indexada; apertura fallida. Ruta oficial de analíticos localizada en búsqueda; apertura devolvió 502.

#### shcp-cuenta-publica

**Cuenta Pública: gasto al cierre** — SHCP.

- **Cobertura y unidad:** Federal y desagregaciones de la base elegida. Clave presupuestaria × ejercicio × momento contable.
- **Periodo / actualización:** Cuenta Pública 2025 identificada. Anual.
- **Acceso y formatos:** Datos abiertos del ejercicio y sus catálogos; descarga pendiente. Formatos: Bases tabulares, Reportes.
- **Variables de interés:** Aprobado; Modificado; Devengado; Pagado; Programa.
- **Llaves para cruzar:** Ejercicio + clave presupuestaria + momento contable.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Diferencia entre asignación y gasto al cierre por sector.
- **Límites:** Homologar llaves y clasificaciones entre ejercicios. Devengado y pagado son conceptos distintos; no sumar momentos contables.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://www.transparenciapresupuestaria.gob.mx/es/PTP/Cuenta_Publica_2025) — Fuente indexada; apertura fallida. Página oficial indexada con datos abiertos; apertura devolvió 502.

#### shcp-srft

**SRFT: ejercicio y destino del gasto federalizado** — SHCP y gobiernos subnacionales.

- **Cobertura y unidad:** Entidades y municipios; proyectos con georreferencia cuando exista. Ejercicio: registro presupuestario; destino: proyecto/ubicación × corte.
- **Periodo / actualización:** Ejercicios y trimestres publicados; último corte no comprobado. Trimestral.
- **Acceso y formatos:** Descargar separadamente Ejercicio del gasto y Destino del gasto. Formatos: Bases tabulares, Anexos.
- **Variables de interés:** Fondo; Municipio; Proyecto; Avance físico/financiero; Coordenadas si existen.
- **Llaves para cruzar:** Ejercicio + trimestre + fondo + entidad/municipio; folio de proyecto en Destino.
- **CP:** Cruce espacial. **Prioridad:** P1. **Esfuerzo:** Alta.
- **Estado:** Por incorporar.
- **Análisis:** Priorizar zonas con carencias y obras rezagadas; gasto escolar y accesibilidad.
- **Límites:** No sumar cortes acumulados trimestrales ni multiplicar monto al expandir ubicaciones. Coordenadas faltantes o de oficina requieren validar destino; no asumir CP nativo.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://www.transparenciapresupuestaria.gob.mx/Entidades-Federativas) — Fuente indexada; apertura fallida. Página oficial indexada describe ejercicio, destino y resultados trimestrales; apertura devolvió 502.
- [Fuente 2](https://www.finanzaspublicas.hacienda.gob.mx/es/Finanzas_Publicas/Informes_al_Congreso_de_la_Union) — Fuente primaria indexada. Página SHCP localizada con el informe de recursos federales transferidos y sus carpetas.

### Educación

#### sep-cct

**Catálogo de Centros de Trabajo** — SEP / SIGED.

- **Cobertura y unidad:** México. Centro de trabajo; revisar servicios y turnos del archivo.
- **Periodo / actualización:** Corte publicado por SIGED; no determinado. Actualización del catálogo; sin frecuencia comprobada.
- **Acceso y formatos:** SIGED anuncia la descarga; los recursos no fueron visibles en lectura estática. Formatos: Descarga anunciada; formato por confirmar.
- **Variables de interés:** CCT; Nombre; Nivel/servicio; Sostenimiento; Ubicación según archivo.
- **Llaves para cruzar:** CCT + turno/servicio cuando aplique + corte.
- **CP:** Por confirmar. **Prioridad:** P1. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Escuelas con baja accesibilidad; cobertura educativa por territorio.
- **Límites:** Confirmar CP y coordenadas en el diccionario antes de tratarlos como disponibles. CCT, turno y servicio pueden producir varias filas por inmueble.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://siged.sep.gob.mx/SIGED/datos_abiertos.html) — Contenido primario leído. Página oficial leída; anuncia Catálogo de Centros de Trabajo y Formato 911. Las tablas de descarga no expusieron archivos en la lectura estática.

#### sep-formato-911

**Formato 911: alumnado, docentes y escuelas** — SEP.

- **Cobertura y unidad:** México, conforme recursos y ciclo. Escuela/servicio o agregado, según archivo × ciclo.
- **Periodo / actualización:** Ciclos disponibles en la fuente; último no determinado. Por ciclo escolar.
- **Acceso y formatos:** Seleccionar recurso por nivel y ciclo en datos.gob.mx o SIGED. Formatos: Bases tabulares, Diccionario.
- **Variables de interés:** Matrícula; Docentes; Grupos; Nivel y modalidad.
- **Llaves para cruzar:** Ciclo + CCT/turno/servicio si el recurso los contiene.
- **CP:** Por confirmar. **Prioridad:** P1. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Razón alumnos/docente y oferta educativa vinculada a transporte.
- **Límites:** No son expedientes individuales de alumnos. Confirmar CCT, granularidad y turnos antes de enlazar; matrícula no mide calidad del aprendizaje.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://www.datos.gob.mx/dataset/registro_alumnado_personal_docente_educacion_basica_media_superior_formato_911) — Fuente primaria indexada. Ficha SEP localizada; requiere revisar recursos y diccionario por nivel/ciclo.
- [Fuente 2](https://siged.sep.gob.mx/SIGED/datos_abiertos.html) — Contenido primario leído. Página oficial leída; anuncia Catálogo de Centros de Trabajo y Formato 911. Las tablas de descarga no expusieron archivos en la lectura estática.

#### anuies-anuario

**Anuario Estadístico de Educación Superior** — ANUIES.

- **Cobertura y unidad:** México. Institución/plantel × programa × ciclo, según exportación.
- **Periodo / actualización:** Ciclos escolares disponibles en el anuario. Por ciclo escolar.
- **Acceso y formatos:** Filtrar y exportar en aplicación; no asumir API pública. Formatos: Consulta interactiva, Exportaciones por confirmar.
- **Variables de interés:** Programa; Matrícula; Egreso; Titulación; Sexo.
- **Llaves para cruzar:** Ciclo + institución/plantel + programa + dimensiones publicadas.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Oferta de carreras y brechas de participación o egreso.
- **Límites:** No dividir egresados entre matrícula como tasa de cohorte. Homologar planteles y carreras; no garantiza CCT o CP.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://anuario.anuies.mx/) — Fuente primaria indexada. Aplicación oficial localizada; su enlace fue confirmado en una página de ANUIES abierta. No se exportaron resultados.

### Movilidad social

#### ceey-emovi-2023

**ESRU–EMOVI 2023** — CEEY / Fundación ESRU.

- **Cobertura y unidad:** Nacional, urbano/no urbano y cinco regiones. Persona entrevistada con retrospectiva del hogar de origen.
- **Periodo / actualización:** 2023. Ola específica.
- **Acceso y formatos:** ZIP enlazado desde la página del productor; formato interno no inspeccionado. Formatos: ZIP de bases, Metodología, Programas de cálculo.
- **Variables de interés:** Origen/destino socioeconómico; Educación; Cuidados; Inclusión financiera.
- **Llaves para cruzar:** ID de entrevista dentro de la ola; región sólo para agregados.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Matrices de transición y brechas de oportunidades.
- **Límites:** Usar factores y metodología de índices; no extrapolar a CP ni alcaldía. Comparar olas exige armonizar variables.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://ceey.org.mx/contenido/que-hacemos/emovi/) — Contenido primario leído. Página del productor leída y enlace BASES DE DATOS 2023 seguido hasta el ZIP en Drive; contenido del ZIP no descargado. [Archivo o recurso localizado](https://drive.google.com/file/d/1r736z5vok0ss68cIW11SnZ5_MR0bUiDC/view?usp=drive_link).

#### ceey-emovi-2017

**ESRU–EMOVI 2017** — CEEY / Fundación ESRU.

- **Cobertura y unidad:** Nacional, cinco regiones y CDMX según diseño. Persona entrevistada y origen familiar retrospectivo.
- **Periodo / actualización:** 2017. Ola específica.
- **Acceso y formatos:** ZIP del productor localizado; contenido no descargado. Formatos: ZIP de bases, Metodología.
- **Variables de interés:** Recursos de origen; Logro educativo; Destino socioeconómico.
- **Llaves para cruzar:** ID de entrevista dentro de la ola; dominios sólo para agregados.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Contrastar movilidad regional y CDMX con 2023 donde sea comparable.
- **Límites:** Encuestas independientes; no es panel de las mismas personas. La representatividad CDMX no habilita desglose por CP.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://ceey.org.mx/contenido/que-hacemos/emovi/) — Contenido primario leído. Página del productor leída y enlace BASES DE DATOS 2017 seguido hasta el ZIP en Drive; contenido del ZIP no descargado. [Archivo o recurso localizado](https://drive.google.com/file/d/1hko58nfnlexpw5kiB1K0kqeXlOPAaGyr/view?usp=sharing).

#### inegi-mmsi-2016

**Módulo de Movilidad Social Intergeneracional 2016** — INEGI.

- **Cobertura y unidad:** México; dominios definidos por diseño muestral. Persona de 25–64 años, presente y retrospectiva a los 14.
- **Periodo / actualización:** 2016. Levantamiento específico.
- **Acceso y formatos:** Microdatos públicos; tabla MMSI_2016 documentada. Formatos: Microdatos, Diccionario, Cuestionario.
- **Variables de interés:** Educación y ocupación actuales; Condición socioeconómica de origen.
- **Llaves para cruzar:** Llave de persona dentro del levantamiento, según diccionario.
- **CP:** No asumir. **Prioridad:** P2. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Persistencia educativa y ocupacional entre generaciones.
- **Límites:** No mezclar índices MMSI y EMOVI como si fueran equivalentes. Ponderadores y dominios de inferencia obligatorios.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.

**Fuentes y verificación:**

- [Fuente 1](https://www.inegi.org.mx/programas/mmsi/2016/) — Fuente primaria indexada. Programa oficial, diccionario y descripción de tabla MMSI_2016 localizados.

#### coneval-pobreza-municipal

**Pobreza municipal 2010–2020** — CONEVAL, archivo histórico.

- **Cobertura y unidad:** Municipios y alcaldías de México. Municipio × año × indicador.
- **Periodo / actualización:** 2010, 2015 y 2020. Cortes de medición publicados.
- **Acceso y formatos:** Descargar bases y metodología del archivo histórico. Formatos: Bases, Programas de cálculo.
- **Variables de interés:** Pobreza; Pobreza extrema; Carencias; Población de referencia.
- **Llaves para cruzar:** Clave entidad (2) + municipio (3) + año.
- **CP:** No asumir. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Estado:** Por incorporar.
- **Análisis:** Distribución de presupuesto por población en pobreza.
- **Límites:** Resultados territoriales, no trayectorias individuales. Revisar cambios municipales y comparabilidad metodológica; no presentar como cifras de 2026.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://www.coneval.org.mx/Medicion/Paginas/Programas_BD_municipal_2010_2020.aspx) — Fuente primaria indexada. Archivo histórico oficial con bases y programas de cálculo municipal localizado.

#### conapo-marginacion-2020

**Índices de marginación 2020** — CONAPO.

- **Cobertura y unidad:** Entidad, municipio, localidad y ámbito urbano, según base. Área geográfica × indicadores de marginación.
- **Periodo / actualización:** 2020. Edición basada en Censo 2020.
- **Acceso y formatos:** Elegir nivel de desagregación y descargar su base. Formatos: Bases tabulares, Notas técnicas.
- **Variables de interés:** Índice y grado; Indicadores socioeconómicos; Población.
- **Llaves para cruzar:** Clave geográfica + nivel + 2020.
- **CP:** Cruce espacial. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Estado:** Por incorporar.
- **Análisis:** Zonas con marginación alta y baja oferta de transporte o escuelas.
- **Límites:** Marginación y pobreza son medidas distintas. La estimación por colonia no es automáticamente CP; documentar equivalencias.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372) — Fuente primaria indexada. Página oficial con bases por entidad, municipio, localidad y ámbito urbano localizada.

### Movilidad

#### metrobus-gtfs

**Metrobús: GTFS estático y tiempo real** — Metrobús / proveedor del feed.

- **Cobertura y unidad:** Red Metrobús CDMX. Estación/viaje programado y vehículo × snapshot.
- **Periodo / actualización:** Snapshots propios; disponibilidad según historial del repo. Captura horaria laboral de realtime; estático semanal en configuración.
- **Acceso y formatos:** API autenticada con secrets existentes del repo. Formatos: GTFS ZIP/CSV, GTFS-Realtime protobuf.
- **Variables de interés:** route_id; stop_id; trip_id; Posición; Hora.
- **Llaves para cruzar:** _snapshot_id + entity_id; trip_id/route_id/stop_id contra la versión GTFS compatible.
- **CP:** Cruce espacial. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Estado:** Implementado; current localizado. Rutas: [`src/historico_api/sources/metrobus.py`](../src/historico_api/sources/metrobus.py), [`data/current/metrobus_vehicle_positions.csv`](../data/current/metrobus_vehicle_positions.csv), [`data/current/metrobus_vehicle_positions_enriched.csv`](../data/current/metrobus_vehicle_positions_enriched.csv).
- **Análisis:** Regularidad observada y accesibilidad a escuelas y servicios.
- **Límites:** Snapshots horarios no reconstruyen cada viaje ni miden puntualidad completa. Tablas estáticas configuradas; no todas tenían CSV current en el árbol revisado.
- **Uso:** Revisar condiciones del proveedor para reutilización y redistribución del feed.

**Fuentes y verificación:**

- [Fuente 1](https://github.com/jcval94/DataCollectionMov/blob/main/src/historico_api/sources/metrobus.py) — Código y árbol revisados. Código de autenticación y recolección leído; rutas de snapshots presentes. No se ejecutó la API autenticada.

#### ecobici-viajes

**ECOBICI: viajes históricos** — ECOBICI / SEMOVI.

- **Cobertura y unidad:** CDMX, área del sistema. Viaje entre cicloestaciones.
- **Periodo / actualización:** Archivos mensuales históricos; página indexa desde 2010. Mensual.
- **Acceso y formatos:** Descarga mensual; recolector ya implementado. Formatos: CSV/ZIP.
- **Variables de interés:** Estaciones de origen/destino; Inicio/fin; Duración; Demografía cuando exista.
- **Llaves para cruzar:** ID de estación origen/destino + periodo de vigencia del catálogo.
- **CP:** Cruce espacial. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Estado:** Recolector; current objetivo no localizado. Rutas: [`src/historico_api/sources/ecobici.py`](../src/historico_api/sources/ecobici.py), [`.github/workflows/ecobici-historical.yml`](../.github/workflows/ecobici-historical.yml).
- **Análisis:** Flujos casa–estudio aproximados y conexiones con Metrobús.
- **Límites:** No se encontró ecobici_historico_normalizado en current durante esta revisión. Cambian esquemas/sistema; una estación cercana a universidad no prueba motivo de viaje.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://ecobici.cdmx.gob.mx/datos-abiertos/) — Fuente primaria indexada. Página oficial de datos abiertos localizada; histórico mensual también indexado en ecobici.mx/datos-abiertos/.

#### ecobici-gbfs

**ECOBICI: catálogo y disponibilidad GBFS** — ECOBICI / SEMOVI.

- **Cobertura y unidad:** CDMX, cicloestaciones del sistema. Cicloestación × snapshot.
- **Periodo / actualización:** Snapshots propios del repositorio. Disponibilidad en origen en tiempo real; repo cada dos horas laborales.
- **Acceso y formatos:** Feeds GBFS y recolección existentes; consultar configuración actual. Formatos: JSON GBFS, CSV derivado.
- **Variables de interés:** station_id; Capacidad; Bicicletas/espacios disponibles; Coordenadas.
- **Llaves para cruzar:** _snapshot_id + station_id.
- **CP:** Cruce espacial. **Prioridad:** P2. **Esfuerzo:** Baja.
- **Estado:** Implementado; current localizado. Rutas: [`data/current/ecobici_gbfs_station_information.csv`](../data/current/ecobici_gbfs_station_information.csv), [`data/current/ecobici_realtime_stations.csv`](../data/current/ecobici_realtime_stations.csv).
- **Análisis:** Frecuencia observada de estaciones vacías cerca de campus y Metrobús.
- **Límites:** Snapshots no son viajes ni disponibilidad continua. Conservar timestamp y estado operativo al comparar estaciones.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://ecobici.cdmx.gob.mx/datos-abiertos/) — Fuente primaria indexada. Página oficial de datos abiertos localizada; histórico mensual también indexado en ecobici.mx/datos-abiertos/.

### Salud y seguridad

#### salud-clues

**CLUES: establecimientos de salud** — Secretaría de Salud / DGIS.

- **Cobertura y unidad:** México. Establecimiento de salud × corte.
- **Periodo / actualización:** Histórico visible desde 2016; enlace septiembre 2026 localizado. Cortes mensuales publicados.
- **Acceso y formatos:** Descarga del histórico oficial; XLSX localizado, filas no inspeccionadas. Formatos: XLSX.
- **Variables de interés:** CLUES; Institución; Tipo/estatus; CP; Coordenadas según corte.
- **Llaves para cruzar:** CLUES + corte; CP como agrupación.
- **CP:** Sí, documentado. **Prioridad:** P1. **Esfuerzo:** Baja.
- **Estado:** Por incorporar.
- **Análisis:** Acceso a unidades de salud por CP y transporte.
- **Límites:** Validar nombres exactos de columnas y unidades activas. Existencia de unidad no implica capacidad, atención efectiva ni calidad.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://gobi.salud.gob.mx/Bases_Clues.html) — Contenido primario leído. Histórico oficial leído; enlace septiembre 2026 resolvió a XLSX no interpretable por el navegador de investigación. [Archivo o recurso localizado](https://gobi.salud.gob.mx/historico_clues/ESTABLECIMIENTO_SALUD_202609.xlsx?v=1.1).
- [Fuente 2](https://www.dgis.salud.gob.mx/descargas/clues/pdf/Manual_registro_informacion_catalogo_CLUES_202506.pdf) — Contenido primario leído. Manual oficial consultado: documenta código postal de cinco dígitos.

#### cdmx-fgj-carpetas

**Carpetas de investigación FGJ CDMX** — FGJ CDMX / portal de datos CDMX.

- **Cobertura y unidad:** Ciudad de México. Registro publicado de carpeta/delito según diccionario.
- **Periodo / actualización:** Desde enero de 2016; último corte sin comprobar. Actualización de la fuente; comprobar corte.
- **Acceso y formatos:** Descarga desde ficha CKAN. Formatos: CSV.
- **Variables de interés:** Delito; Fecha de hechos/apertura; Alcaldía; Colonia; Coordenadas.
- **Llaves para cruzar:** ID de registro si existe; fecha y coordenadas para agregados.
- **CP:** Cruce espacial. **Prioridad:** P2. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Incidencia registrada en entornos de escuelas y estaciones.
- **Límites:** No son todos los delitos: hay subregistro y cambios de clasificación. Usar denominadores de exposición; comparar hechos con hechos y aperturas con aperturas.
- **Uso:** Conservar atribución y revisar los términos del recurso antes de redistribuir la base.

**Fuentes y verificación:**

- [Fuente 1](https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico) — Fuente primaria indexada. Ficha FGJ oficial localizada: registros desde enero 2016 y variables geográficas; no se comprobó último mes.

#### inegi-atus

**ATUS: accidentes de tránsito urbanos y suburbanos** — INEGI.

- **Cobertura y unidad:** México; cobertura de reporte y georreferenciación variable. Accidente reportado.
- **Periodo / actualización:** Serie anual; coordenadas desde 2019 en municipios seleccionados. Anual.
- **Acceso y formatos:** Descargar año y diccionario desde programa. Formatos: CSV, Documentación.
- **Variables de interés:** Tipo; Hora; Municipio; Lesionados/fallecidos según registro; Usuarios involucrados.
- **Llaves para cruzar:** ID/llave definida por edición; entidad + municipio + año.
- **CP:** Cruce espacial. **Prioridad:** P2. **Esfuerzo:** Media.
- **Estado:** Por incorporar.
- **Análisis:** Seguridad vial alrededor de escuelas y conexiones de transporte.
- **Límites:** No asumir cobertura carretera federal ni coordenadas para todos los municipios. Revisar notas por año/municipio antes de comparar tasas.
- **Uso:** Términos INEGI: https://www.inegi.org.mx/inegi/terminos.html; conservar atribución, edición y metadatos.

**Fuentes y verificación:**

- [Fuente 1](https://www.inegi.org.mx/programas/accidentes/default.html) — Fuente primaria indexada. Programa ATUS oficial localizado; georreferenciación desde 2019 sólo para municipios seleccionados.

## Incorporación posterior y mantenimiento

Antes de implementar una fuente: descargar una muestra o archivo, identificar corte y licencia, guardar diccionario y URL exacta, comprobar llaves/cobertura y definir si merece histórico. Para archivos grandes, usar almacenamiento de datos adecuado y versionar aquí el manifiesto o muestra permitida.

En una siguiente revisión actualizar primero `catalogs/datasets_reales_mexico.json` y reflejarlo en este documento. No añadir una entrada a `configs/tables.yml` hasta que exista un recolector o una carga manual reproducible y documentada. Los recolectores existentes siguen usando su configuración actual.
