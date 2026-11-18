# Diccionario · NASA PS

Grano: un planeta y su conjunto de parámetros por defecto en PS (`default_flag=1`), con descubrimiento hasta 2025. Las mediciones son las disponibles al adquirir en noviembre de 2026. No se mezcla PSCompPars. El snapshot mide 6,090 filas y 29 columnas, reconciliadas con una consulta de conteo independiente.

| Campo | Tipo / unidad | Regla |
| --- | --- | --- |
| pl_name | Texto; llave única | No confundir planeta con hostname |
| hostname | Texto; estrella/sistema anfitrión | Repetición legítima en sistemas múltiples |
| default_flag | Entero booleano | Siempre 1 en esta selección |
| discoverymethod, disc_facility | Categorías del archivo | Método de descubrimiento, no todos los métodos que luego detectaron el planeta |
| disc_year | Año entero | <=2025; no fecha de actualización de la medida |
| pl_controv_flag | 0/1 | Se conserva, no borra planetas cuestionados |
| pl_orbper | Días | Periodo orbital positivo |
| pl_rade | Radios terrestres | No mide habitabilidad |
| pl_eqt | Kelvin | Temperatura de equilibrio modelada, no superficie |
| pl_bmasse, pl_bmassprov | Masas terrestres y procedencia | Puede ser masa o masa mínima; no se usa como masa homogénea en clustering |
| sufijo lim | -1 / 0 / 1 / vacío | Límite inferior / medida / superior / no informado; sólo 0 entra a análisis de medidas |
| sufijos err1, err2 | Misma unidad que la medida | Error superior positivo e inferior negativo; no reemplazar faltantes con cero |
| sy_dist | Parsecs | Distancia de la estrella, no separación de planeta y estrella |
| pl_refname, st_refname, sy_refname | Referencias originales | HTML del proveedor conservado como texto, nunca ejecutado |
| rowupdate | Fecha de actualización del registro | No fecha de descubrimiento ni garantía de disponibilidad histórica |

Campos derivados de Silver: `*_measured` exige valor positivo y lim=0; `*_errors_usable` exige errores firmados válidos y límite inferior positivo. `cluster_eligible` exige radio, periodo y temperatura utilizables; `log10_*` transforma unidades estrictamente positivas. Las filas originales permanecen en Silver. Gold incluye exclusivamente tablas específicas; el archivo clustered contiene casos completos y grupos exploratorios ordenados por radio logarítmico medio.

Ausencias se conservan. Las cotas de radio asignan los valores no medidos a extremos dentro/fuera; no son intervalos de confianza. El archivo no contiene no detecciones, costos, solicitudes a observatorios ni completitud de búsqueda. No permite prevalencia del universo, causalidad o eficiencia monetaria.
