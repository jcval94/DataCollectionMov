# Lote 1C · NYC Rodent Inspections

Incremento sobre NASA (#6), sin sustituir OpenFlights ni los tres pilotos. Ventana cerrada de inspecciones de 2024 en p937-wjvj de NYC DOHMH / NYC Open Data: 234, 596 filas, seis campos solicitados y 20, 791, 476 bytes originales. Una consulta independiente con el mismo filtro devuelve234, 596; el límite500, 000 no truncó la selección. Snapshot gzip sin pérdida, consulta ordenada, fecha de adquisición, bytes y hashes originales/comprimidos en el manifiesto. La base puede corregir registros históricos: no se presenta como conocimiento disponible al cierre de 2024.

## Fuente, derechos y privacidad

El [manual oficial](https://www.nyc.gov/content/dam/nycgov/opendata/downloads/open-data-coordinators/NYC_OpenData_TechnicalStandardsManual.pdf), sección 2.3.2, describe las bases publicadas de NYC Open Data como recurso público sin requisito de licencia. Se consultaron la [ficha de Rodent Inspection](https://data.cityofnewyork.us/Health/Rodent-Inspection/p937-wjvj/about_data) y los [términos generales](https://www.nyc.gov/main/terms-of-use). El manifiesto registra hash del PDF completo y distingue el hash de JSON de metadata normalizado de los bytes HTTP originales. No se inventa una licencia CC ni permiso sobre diseño o imágenes del sitio.

Se conserva atribución y advertencia del productor: no inspeccionado no significa ausencia de ratas; más inspecciones pueden producir más hallazgos. La consulta no solicita direcciones, coordenadas, nombres u observaciones libres. BBL es una llave catastral pública, **no anonimizada**; se conserva para reproducibilidad, sin publicar mapas de predios. Todas las tablas Gold del alumno son agregadas. No hay consejo sanitario ni recomendación presupuestal.

## Preprocesamiento y calidad

Silver conserva las 234, 596 filas. Diez copias exactas se señalan y sólo se retiran de denominadores Gold, dejando234, 586 eventos únicos. La llave administrativa candidata combina job_id+fecha+tipo+bbl; conflictos no idénticos detienen el proceso, no se escoge un resultado conveniente.

Se distinguen visitas iniciales, seguimientos, tratamientos, sellados y limpiezas. Tratamiento no significa resultado negativo. El resultado positivo corresponde exactamente a las dos categorías de señales de actividad de ratas; otros fracasos son negativos respecto de esa señal, no certificación de ausencia de animales.

Hay 5, 830 BBL ausentes/inválidos y 202 registros con BBL válido que contradice el borough. No se reparan ni se trasladan por suposición. Se mantienen en análisis de eventos según su borough declarado y se excluyen sólo del emparejamiento por predio. Los motivos pueden solaparse con otros filtros. La política por predio parte de 149, 993 eventos iniciales con llaves coherentes y usa la primera visita observada en 2024, ordenada por fecha y job_id sin elegir por resultado.

Se obtienen154, 631 eventos iniciales únicos y 99, 462 primeros predios; 4, 638 eventos iniciales quedan fuera del universo de llaves coherentes. El perfil incluye tipos, fechas, memoria, tamaño, nulos, cardinalidad, duplicados, cobertura, categorías y reglas. Timestamps flotantes: se usa calendario del productor, sin inventar una conversión UTC. Silver comprimido sin pérdida mantiene cada archivo dentro del límite de ejecución.

## Preguntas y resultados comprobados

Seis contratos específicos. B se **acota expresamente a boroughs** y conserva la pregunta original sobre barrios como antecedente; no hay barrio o geometría para contestarla a esa resolución. C, D1 y E también se ejecutan. A sigue bloqueada por costos/horas ausentes; D2 por no observar población real de roedores ni todos los periodos. El catálogo archivado de 86 fuentes/516 preguntas no se reescribe; el overlay de agentes presenta la formulación operativa.

| Ruta | Ejecución y límite |
| --- | --- |
| D04-B | Primeras inspecciones positivas / primeros predios con llave coherente, por borough. Contrastar todos los eventos iniciales y sólo eventos con la misma política de llaves antes de cambiar la unidad |
| D04-C | Doce meses y 60 celdas borough/mes; conteos y tasas con denominador propio. Un año no prueba estacionalidad recurrente |
| D04-D1 | Verano jun/jul/ago frente a invierno ene/feb/dic del mismo2024; tasas dentro de cada borough, pesos iguales y cohorte pareada. No efecto causal del calor |
| D04-E | Cinco políticas: iniciales, iniciales con llaves coherentes, primera visita por predio, cualquier positivo por predio e iniciales+seguimientos. Conteo y tasa responden preguntas distintas |

Resultados concretos del snapshot:

- Brooklyn tiene 13, 887 iniciales positivas, el mayor conteo, pero su tasa de primeras visitas por predio es8, 855/42, 528 =20.82%. Bronx tiene 8, 541 iniciales positivas, pero4, 217/16, 650 =25.33% de primeros predios positivos. No se traduce ese orden en población real de ratas.
- En eventos iniciales, invierno tiene 25.23% de positivos y verano20.92%: diferencia aproximada−4.30 puntos porcentuales. Los cinco boroughs muestran diferencia negativa en esa comparación descriptiva; se conservan sus denominadores.
- En los mismos18, 007 predios observados en ambas estaciones, la diferencia es−0.655 puntos porcentuales. El bootstrap condicional de 500 remuestreos da aproximadamente[−1.322, 0.012] pp; con 2, 000 da[−1.283, 0.000] pp. El borde cercano a cero no justifica una afirmación categórica de significación.
- En5, 320 de esos predios la primera visita de invierno es en diciembre. Por eso el cruce invierno/verano **no es una transición cronológica**. Restringir invierno a enero/febrero cambia la cohorte a 12, 687 predios y la diferencia a−1.253 pp; bootstrap condicional aproximado[−2.078,−0.402] pp. Cambiar ventana y cohorte cambia la pregunta; no se oculta.

Bootstrap pareado por predio, semilla 1729. Supone remuestreo IID de la cohorte seleccionada; no corrige dependencia espacial ni selección por quejas/inspección proactiva. No se extrapola a población ni se calcula un p-valor confirmatorio o un efecto de intervención.

## Visuales, narrativa y experiencia

Siete figuras: alcance por tipo, tres denominadores por borough, heatmap mensual, diferencias estacionales, sensibilidad de cohortes e intervalos pareados, ranking por métrica y volumen mensual. PNG/SVG en móvil/proyección; fuentes, periodo, denominadores, notas, texto alternativo y hashes de código/snapshot/tabla. La inspección real detectó etiquetas de eje móvil solapadas y una barra de color fuera del lienzo: se simplificaron ticks y se pasó la escala de color a horizontal. El heatmap declara su rango lineal común; las diferencias usan puntos porcentuales y referencia cero.

Cuatro narrativas específicas, siete actos cada una, decisiones de investigación, límites, bifurcaciones, transferencia y screencast de 55 minutos. La galería exige predicción antes de mostrar figuras; no transmite ni conserva respuestas. Kit alumno ejecutable sin red, contingencia precalculada, diccionario, derechos y tablas agregadas. Guiones específicos, referencias y ensayo docente se generan en teacher/, fuera de los ZIP y uploads de alumno.

La incorporación del adaptador cambia la versión del runner compartido. La cache incluye el código empaquetado de todos los adaptadores y requirements. Se regeneran y revisan los catorce PNG de NASA con su nueva referencia de código y marcadores de forma además de color; sus datos, resultados numéricos y tablas permanecen intactos. Se conservan las evidencias previas en el historial Git y el PR de NASA sigue siendo independiente y revisable.

## Verificación y operación

```sh
python -m pip install -r discovery_labs/requirements-batch1.txt
python discovery_labs/scripts/prepare_fieldlab.py --case nyc-ratas
python discovery_labs/scripts/run_fieldlab.py --case nyc-ratas
python -m unittest discover -s discovery_labs/tests -v
python discovery_labs/tests/fieldlab_browser.py --case nyc-ratas
python discovery_labs/scripts/agent_tools.py run --case nyc-ratas --question D04-D1
```

Cinco pruebas nuevas con fixtures manuales y snapshot: llaves faltantes, duplicados, tratamiento no negativo, selección por fecha sin resultado, conflictos de negocio y fecha futura rechazados, pareado de incertidumbre conocida, diciembre posterior al verano, reconciliación y paquete ejecutado en otro proceso/hash seed. Se comparan resultados, CSV y PNG; manifiesto del kit comprobado y ausencia de archivos docentes. Suite acumulada: 27 tests. Chromium añade ocho combinaciones pregunta/pantalla y catorce capturas, sin red, errores JS ni overflow.

Pipeline determinista con staging, cache verificada, errores estructurados y snapshots previos conservados. Interfaz de agentes: acciones permitidas, red bloqueada, sin tokens heredados ni código arbitrario, 4 GiB, 50 s CPU, 60 s pared y 32 MiB por archivo. Ejecución local del orden de 9 segundos, sin acreditar duración de aula. La opción de ingesta `--download` exige bytes exactos del manifiesto y falla sin reemplazar el snapshot si el servicio vivo cambió.

`DATA_READY` y cuatro rutas con investigación/visual/narrativa verificadas. `CLASS_READY` y `PUBLISHED` cerradas: faltan ensayo humano observado y revisión docente independiente. No se libera material al curso ni se modifican calendario, precios, misiones o evaluación.

## Progreso acumulado de los incrementos

| Dimensión | Lote 1 | Biblioteca |
| --- | --- | --- |
| Inventario | 7 candidatos conservados | 86/86 =100% |
| Fuentes procesadas | 3/7 =42.9% | 6/86 =7.0% |
| Contratos específicos | 18/42 =42.9% | 36/516 =7.0% |
| Preguntas ejecutadas | 12/42 =28.6% | 24/516 =4.7% |
| Preguntas con figuras revisadas | 12/42 =28.6% | 24/516 =4.7%; 38 figuras distintas |
| Narrativas ejecutadas | 12/42 =28.6% | 24/516 =4.7% |
| Aprobación pedagógica | 0/7 | 0/86 |

Las otras cuatro fuentes del lote mantienen sus bloqueadores; no se declara completo. Evidencia estructurada: `evidence/v3/fieldlab/nyc-ratas/`. Los enlaces y estado final de CI se registran en el PR en borrador.
