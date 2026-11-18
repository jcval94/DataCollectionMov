# OpenFlights · diccionario y contrato de datos

Fuente: OpenFlights, tablas completas `airports.dat` y `routes.dat` del commit fijado en `data/manifest.json`. Formato CSV sin cabecera del productor, comprimido sin pérdida con gzip determinista. La huella compuesta y las huellas por archivo permiten recuperar exactamente los bytes originales. Licencia de base y derivados: ODbL-1.0; contenidos ODC-DbCL-1.0. El texto de licencia del productor está en `data/LICENSE`.

## Aeropuertos: una fila por ID

| Campo | Tipo Silver | Unidad y regla |
| --- | --- | --- |
| airport_id | Texto | Llave única numérica como texto, no IATA |
| name | Texto | Nombre del aeropuerto en la metadata fijada |
| city, country | Texto | Ciudad y país declarados; no límites cartográficos ni regiones oficiales de comunidad |
| iata, icao | Texto | Códigos; `\N` significa ausente. Pueden diferir del código que acompaña a una ruta histórica |
| latitude, longitude | Float | Grados WGS84; latitud −90 a 90, longitud −180 a 180. Cero es una coordenada válida |
| altitude_ft | Texto original | Pies; conservado, no se usa para distancia ni centralidad |
| timezone_offset, dst, timezone | Texto original | Metadata horaria; no se usa para reconstruir horarios de vuelo |
| type, metadata_source | Texto | Tipo y procedencia declarados por productor |

## Rutas: una fila de compañía y conexión, no un vuelo

| Campo | Tipo Silver | Unidad y regla |
| --- | --- | --- |
| airline, airline_id | Texto | Compañía y su ID; no se necesita tabla de marcas o imágenes |
| source_iata, destination_iata | Texto | Códigos originales para auditar desacuerdos, sin usarlos como llaves supuestas |
| source_id, destination_id | Texto | Llaves hacia airport_id; `\N` o huérfanos se señalan y se excluyen sólo de Gold |
| codeshare | Texto | Y si hay código compartido; vacío es no marcado, no falta de arista |
| stops | Entero | Escalas no negativas. Gold de conexión directa conserva sólo 0 |
| equipment | Texto original | Códigos de equipos; no permiten estimar capacidad ni frecuencia |

Silver conserva todas las filas y añade `raw_row_id`, `eligible`, `exclusion_reason` y banderas de desacuerdo de IATA. No se deduplican ni remapean aeropuertos por intuición. Varias filas pueden describir una misma arista por aerolíneas o código compartido.

Gold contiene una fila por par dirigido source_id→destination_id de cero escalas, con `route_records`, `distinct_airlines` y `codeshare_records`. Esos conteos no se usan como peso de pasajeros. Para grado, comunidades y accesibilidad se proyecta el grafo a conexiones binarias no dirigidas; intermediación se calcula también en la versión dirigida.

Grado = número de vecinos distintos. Intermediación = proporción de caminos mínimos que pasan por el nodo; aproximada con 128 pivotes y semilla fija, contrastada con 64. ARI compara asignaciones de comunidades, no su verdad geográfica. Spearman se calcula sobre valores con manejo de empates; los rankings ordinales desempatan por ID para poder reproducir tablas.

Distancia = Haversine, radio terrestre 6371.0088 km, entre coordenadas de dos aeropuertos activos. Umbral principal 250 km y sensibilidad 100/500 km. El denominador es el total de pares no ordenados que cumple cada umbral; una conexión en cualquier dirección basta para este contraste.

En resiliencia por país, el universo inicial es el componente gigante no dirigido y se requiere ≥5 aeropuertos del país. Tras retirar un aeropuerto, éste sale del denominador: sólo otros aeropuertos que dejan el nuevo componente gigante se cuentan como desconectados. El baseline retira hasta 20 nodos locales distintos uniformemente, con semilla fija; su media no es intervalo de confianza ni efecto en pasajeros.

## Cobertura y límites

El productor informa que el proveedor de rutas dejó de actualizar en junio de 2014. La metadata de aeropuertos procede del mismo commit de archivo, pero su vigencia no es un censo comprobado de 2014. Se mide integridad de llaves y se registra desacuerdo de códigos, sin atribuir contemporaneidad a ambas tablas. No hay fecha por vuelo, horarios, demanda, precios, capacidad, pasajeros ni respuesta operativa de compañías. Ningún mapa representa rutas actuales ni sirve para navegación.
