# Lote 1A · OpenFlights ejecutado

Corte local: 17 de noviembre de 2026. Extensión pequeña y verificable sobre el PR V3 #3. Se comprobó además que la CI del contrato educativo, mvp-ds-course PR #102, terminó en éxito: [run 44031984325](https://github.com/jcval94/mvp-ds-course/actions/runs/44031984325). Ninguna clase se aprueba o publica por ese hecho.

## Alcance del incremento

Se procesa la primera de las siete fuentes del Lote 1. Las otras seis conservan el preflight y sus puertas abiertas; no se declaran procesadas por transitividad. OpenFlights tiene seis contratos específicos, cinco ejecutados y uno bloqueado: oportunidad comercial exige demanda, tarifas, capacidad y costos ausentes. Los 86 IDs y 516 diseños del inventario permanecen intactos. La interfaz de agentes superpone estados por ID sin reescribir la evidencia anterior.

El adaptador de grafos es nuevo; los archivos y el código de los tres pilotos del Lote 0 se conservan. Se comparte lectura de manifiestos, recibos, escritura estructurada y generación de materiales. No se aplican transformaciones de Retail, NBA o Bob Ross a una red de rutas.

## Datos realmente recibidos y decisiones

| Capa | Medición y regla |
| --- | --- |
| Bronze | 7,698 filas y 14 campos de aeropuertos; 67,663 filas y 9 campos de rutas; licencia del productor |
| Versión | Commit upstream `cd163fa17710f3135540651626ad719dd5322a05`; gzip sin pérdida y hashes de bytes comprimidos/originales |
| Silver | Todas las filas originales, IDs y banderas de elegibilidad; coordenadas WGS84 y escalas numéricas |
| Exclusiones señaladas | 483 orígenes sin llave resuelta, 488 destinos sin resolver, 11 rutas con escalas y 19 lazos propios; motivos pueden solaparse |
| Gold | 66,759 registros elegibles reconciliados en 36,906 conexiones dirigidas únicas entre 3,214 aeropuertos |
| Proyección no dirigida | 18,858 conexiones binarias; no pesos de pasajeros o frecuencia |
| Metadata | 1,075 registros con desacuerdos de IATA; no se infieren llaves a partir de códigos |

El productor dice que el proveedor de rutas dejó de actualizar en junio de 2014. La metadata de aeropuertos está congelada en el mismo commit, pero no es un censo comprobado de 2014. Se explicita ese límite y se analiza una política alternativa de coincidencia de códigos manteniendo nodos y pares fijos. Las coordenadas son válidas en su rango; eso no prueba contemporaneidad del servicio.

Vacío en `codeshare` significa no marcado, no dato perdido. Los perfiles distinguen ese significado de `\N`, conservando por separado el número de vacíos. No se eliminan observaciones por parecer valores extremos ni se borran duplicados de Bronze/Silver. Varias aerolíneas o códigos compartidos se colapsan sólo al construir la adyacencia binaria.

## Derechos y distribución concreta

Se conserva el `data/LICENSE` del commit, ODbL-1.0, y la atribución al proveedor. Las tablas originales/derivadas mantienen ODbL-1.0 y contenidos ODC-DbCL-1.0. Se incluyen avisos y licencia en el kit. No se copian imágenes de mapas, logos ni las tablas de aerolíneas/aviones; las figuras son generadas por este código.

Fuentes primarias consultadas: [datos, cobertura y condiciones del productor](https://openflights.org/data.php), [licencia en el repositorio](https://github.com/jpatokal/openflights/blob/cd163fa17710f3135540651626ad719dd5322a05/data/LICENSE), [ODbL-1.0](https://opendatacommons.org/licenses/odbl/1-0/). La licencia específica de la base se aplica con sus condiciones; no se infiere permiso para usar imágenes comerciales del sitio por existir una descarga de datos.

## Investigación y pruebas adversariales

| Pregunta | Método, base y límite |
| --- | --- |
| D16-B | Retiro del hub local frente a hasta 20 retiros locales uniformes sin reemplazo, semilla fija. 99 países con ≥5 nodos en el gigante inicial; el nodo retirado sale del denominador |
| D16-C | Louvain sin pesos sobre proyección no dirigida. Resoluciones 0.8/1.0/1.2 y 20 particiones aleatorias con los mismos tamaños sobre el mismo grafo |
| D16-D1 | Grado exacto frente a intermediación dirigida aproximada con 128 pivotes; contraste con 64, Spearman, Jaccard top10 y primeros puestos separados |
| D16-D2 | Haversine, pares no ordenados activos; umbral principal 250 km y sensibilidad 100/500 km. Base de todos los pares y política alternativa de códigos |
| D16-E | Comparación dirigida/no dirigida, retiros de 0/1/5/10 hubs del ranking original y sensibilidad a códigos coincidentes |

Las etiquetas enteras internas de Louvain evitan que el hash aleatorio de strings de Python cambie la partición. La reproducción se comprueba también desde un proceso independiente con otro `PYTHONHASHSEED`. Intermediación sigue siendo una aproximación con pivotes: una correlación alta no acredita un primer puesto estable.

Resultados de referencia del snapshot, sin inferencia de tráfico actual:

- A ≤250 km hay 1,507 pares conectados entre 10,594 pares elegibles: 14.225%. Exigir además códigos coincidentes deja 1,496/10,594: 14.121%. El denominador permanece fijo; ambas políticas se conservan.
- Los líderes por grado e intermediación difieren. La primera posición de intermediación cambia al pasar de 128 a 64 pivotes, aun con Spearman aproximadamente 0.985 entre esas aproximaciones. No se proclama un aeropuerto universalmente más importante.
- En resolución 1.0 aparecen 25 comunidades y modularidad aproximadamente 0.659; el número cambia con resolución. El contraste aleatorio es exploratorio después de optimizar Louvain, no un p-valor confirmatorio ni prueba de regiones naturales.
- Al retirar diez hubs del ranking original quedan 75 de 3,204 aeropuertos fuera del mayor componente. Se muestran también el escenario inicial y los denominadores; no se llama colapso al resultado ni se simula una reacción de aerolíneas.

La CI detectó que el constructor V2 adoptaba cualquier manifiesto de una carpeta nueva y suponía su esquema de tabla única. Se restringió su registro a los tres pilotos V2: el catálogo archivado se reconstruye sin diferencias y los adaptadores nuevos entran por la interfaz tipada V3. Una regresión aislada prueba que OpenFlights no hereda esquema, derechos ni disponibilidad del constructor antiguo. No se relajaron validadores.

Las cifras completas, incluidos cambios de política, están en los JSON de evidencia y CSV regenerables. No se estima rentabilidad, demanda no atendida, pasajeros afectados, causalidad o conectividad actual.

## Figuras y materiales producidos

Diez figuras distintas, cada una con PNG/SVG de proyección y móvil: atlas por coordenadas, red agregada de comunidades, sensibilidad de resolución, comparación de modularidad, fragilidad por país, grado/intermediación, rankings, cercanía geodésica, sensibilidad de metadata y retiro de hubs. Cada figura vincula preguntas, CSV, código, snapshot, periodo, unidades, denominador, notas y texto alternativo.

La revisión de renderizados corrigió recortes de títulos y solapamientos de leyendas/anotaciones móviles. La comparación de modularidad usa media/rango anotados para que el baseline estrecho no desaparezca al lado del observado. La red dibuja y declara los veinte flujos principales; las tablas conservan todos los flujos. El mapa no descarga bases externas y no representa trayectorias reales.

Cinco narrativas específicas tienen gancho, siete actos, dos caminos, tablas/figuras por momento, prueba de refutación, bifurcaciones y transferencia. Cada una tiene modo screencast de 55 minutos, separado de la clase de 45 minutos. Las complicaciones proceden de los datos y las aproximaciones observadas, sin sorpresa obligatoria.

El kit de alumno tiene snapshot, manifiesto, diccionario, avisos de licencia, galería sin conexión, CSV y motor ejecutable. El kit docente se genera en `teacher/`, con guion, referencias y registro de ensayo, y no se incluye en ZIP ni upload público de CI. No hay respuestas de retos evaluados ni cambios de evaluación del curso.

## Reproducir y usar con agentes

```sh
python -m pip install -r discovery_labs/requirements-batch1.txt
python discovery_labs/scripts/prepare_openflights.py --download
python discovery_labs/scripts/run_batch1.py --case openflights-red-aerea
python -m unittest discover -s discovery_labs/tests -v
python discovery_labs/tests/batch1_browser.py
python discovery_labs/scripts/agent_tools.py catalog
python discovery_labs/scripts/agent_tools.py run --case openflights-red-aerea --question D16-D2
```

La ingesta ocurre antes de clase y reproduce bytes fijados; no busca versiones nuevas. La investigación bloquea red. La interfaz de agentes conserva la lista de comandos permitidos, memoria de 4 GiB, 50 s de CPU, 60 s de pared, archivos de hasta 32 MiB y entorno sin tokens heredados. Rechaza D16-A y preguntas ajenas. No recibe código arbitrario. La ejecución local del snapshot tarda del orden de 15–17 segundos en este entorno; eso no prueba duración de aula.

La cache verifica manifiesto, snapshots, contrato, diccionario, código propio/compartido, Python y dependencias, incluida Pillow. Se promueve una salida nueva sólo al terminar; el error queda estructurado y la salida íntegra anterior permanece. Los archivos de ingesta se sustituyen atómicamente después de validar todos los bytes.

## Validación y puertas

Los 17 tests combinan las 11 comprobaciones anteriores y seis pruebas nuevas: hashes comprimidos/originales, llaves y colapso, coordenadas/dominios, antimeridiano, denominador tras retiro, preservación de catálogo, rutas bloqueadas, repetición exacta y ejecución del ZIP fuera del repositorio con otra semilla de hash. Chromium comprueba cinco preguntas en dos tamaños: diez combinaciones, veinte capturas, imágenes, enlaces CSV, apuesta previa, cero red, cero errores JS y sin overflow horizontal. Los renderizados fueron inspeccionados; los hashes se guardan en `evidence/v3/batch1a/visual-review.json`.

La revisión visual del asistente no es ensayo humano ni revisión docente independiente. Hay cinco rutas con `RESEARCH_READY`, `VISUAL_READY` y `STORY_READY`; `CLASS_READY` y `PUBLISHED` permanecen cerradas. D16-A no recibe aprobación por compartir fuente. Este candidato tiene cinco opciones, no una clase aprobada con seis preguntas votables.

## Progreso sin porcentaje global único

| Dimensión | Lote 1 completo (7 fuentes, 42 perspectivas) | Biblioteca (86 fuentes, 516 perspectivas) |
| --- | --- | --- |
| Inventario | Siete candidatos conservados | 86/86 = 100% |
| Procesamiento validado | 1/7 = 14.3% | 4/86 = 4.7% |
| Contratos específicos nuevos | 6/42 = 14.3% | 24/516 = 4.7% incluyendo Lote 0 |
| Investigación ejecutada | 5/42 = 11.9% | 17/516 = 3.3% |
| Preguntas con figuras revisadas | 5/42 = 11.9% | 17/516 = 3.3%; 24 figuras distintas en total |
| Narrativas con ejecución | 5/42 = 11.9% | 17/516 = 3.3% |
| Aprobación pedagógica | 0/7 = 0% | 0/86 = 0% |

No se declara terminado el Lote 1 ni se libera el curso. El resto conserva las condiciones de acceso/derechos de su preflight; StatsBomb mantiene la restricción de distribución registrada y el sustituto operativo aún necesita snapshot validado. Próxima slice técnica: cerrar derechos y fijar una segunda fuente, aplicando su contrato propio. Próximo paso humano: ensayo observado y revisión docente de una ruta candidata, sin guardar respuestas personales en Git.
