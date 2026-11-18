# Lote 1B · NASA Exoplanetas

Incremento sobre OpenFlights (#4), conservando catálogo y snapshots anteriores. Fuente: tabla PS del NASA Exoplanet Archive, consulta completa `default_flag=1 and disc_year<=2025`, ordenada por planeta. Se recibieron 6,090 filas, 29 columnas y 3,549,129 bytes originales; conteo independiente del servidor: 6,090. Compresión sin pérdida, hashes de original/comprimido, consulta, fecha, versiones, referencias y recibos de documentación están en el manifiesto.

## Derechos y alcance

La FAQ del productor permite investigación adicional con reconocimiento, y su política de publicaciones pide atribuir archivo y referencias de mediciones. Se distribuyen hechos numéricos seleccionados y gráficos originales, con referencias por fila. No se inventa licencia CC ni se extiende permiso a imágenes, logos, artículos o encuestas con condiciones propias. Véase `pilots/nasa-exoplanetas/data/RIGHTS.md` y [FAQ](https://exoplanetarchive.ipac.caltech.edu/docs/faq.html), [atribución](https://exoplanetarchive.ipac.caltech.edu/docs/acknowledge.html), [esquema](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html).

El filtro de descubrimientos hasta 2025 no convierte el archivo en una fotografía histórica de los parámetros al cierre de ese año: las medidas son las vigentes al adquirir en noviembre de 2026. No se usa para pronosticar. PS conserva un conjunto por defecto y referencia, sin completar valores con PSCompPars.

## Preprocesamiento y perfil

Silver conserva las 6,090 filas y los campos originales; convierte numéricos y añade banderas. Los valores positivos sólo se tratan como medidas si `lim=0`. Los límites superiores/inferiores, flags ausentes y errores faltantes no se convierten en puntos medidos o ceros. Los errores asimétricos se conservan firmados. Masa y masa mínima no se mezclan como una sola magnitud para clustering.

Hay 4,542 radios utilizables. Sólo 1,468 filas tienen radio, periodo y temperatura utilizables: 4,622 quedan fuera del clustering, pero permanecen en Bronze/Silver. La completitud varía por método de descubrimiento. El perfil contiene nulos por campo, tipos, memoria, tamaño, cardinalidad, duplicados, cuantiles, valores extremos señalados, unidades, años y referencias. Silver se escribe en gzip sin pérdida para mantener acotado el tamaño de cada archivo; Gold contiene tablas por pregunta.

## Contratos e investigaciones

Seis contratos de 14 componentes. C, D1 y E ejecutados; A (costos/exposición), B (acceso a observatorios) y D2 (completitud/no detecciones) bloqueados. No se confunde un conteo de descubrimientos con eficiencia, equidad o frecuencia de planetas en el universo.

| Ruta | Ejecución y prueba adversarial |
| --- | --- |
| D05-C | Log10 de radio, periodo y temperatura; StandardScaler y K-means k=3, 20 inicializaciones, semilla 1729. Comparar k2/k4, RobustScaler y retirar temperatura sobre las mismas 1,468 filas. Silhouette en muestra fija de hasta 800; ARI respecto de la referencia |
| D05-D1 | Rango operativo 0.8–1.25 radios terrestres; alternativas 0.9–1.1 y 0.75–1.5. Denominador de radios medidos frente a cotas asignando valores no medidos fuera/dentro del rango; errores publicados separados |
| D05-E | Cruce grupo/método y NMI; 50 barajados de método conservan tamaños y filas. Comparación exploratoria, sin p-valor confirmatorio ni identificación causal |

Resultados del snapshot: 471/4,542 = 10.37% de radios centrales medidos cae en el rango principal. Las cotas por no medidos sobre 6,090 filas son 7.73%–33.15%; no incluyen incertidumbre de todos los radios ni prueban habitabilidad. Hay 4,161 filas con errores utilizables: 188 intervalos publicados totalmente dentro del rango y 759 lo solapan; no se supone un nivel de confianza común.

Los tres grupos tienen 468, 448 y 552 casos. ARI al usar escalado robusto: aproximadamente 0.378; sin temperatura: 0.744. Son particiones sensibles, sin validación física externa. NMI de grupo/método aproximadamente 0.0094, frente a media barajada 0.0052 y rango 0.0032–0.0108. **El resultado no sostiene una separación fuerte por método dentro de los casos completos**; sí revela una selección previa muy desigual por completitud. Ambas observaciones se conservan, sin forzar un giro narrativo.

## Visuales y clase candidata

Siete figuras distintas: cobertura por método, mapa radio/periodo, composición de grupos, sensibilidad de particiones, fracciones por umbral de radio, errores asimétricos y cronología de descubrimientos. Cada figura tiene PNG y SVG móvil/proyección, fuente, periodo, denominador, notas, alt y hashes de código/snapshot/tabla. Se inspeccionaron los catorce PNG y capturas Chromium. La etiqueta móvil extensa que fallaba el control de límites se corrigió con salto de línea.

Tres historias con siete actos, preguntas al público, decisiones, prueba adversarial y transferencia; modo screencast de 55 minutos. La galería exige apostar antes de revelar evidencia, no guarda respuestas y funciona sin red. Kit alumno: datos, derechos, diccionario, tablas, código permitido y galería. Kit docente: guion específico, referencias y checklist de ensayo; se genera fuera del ZIP y upload de alumno. No se alteran evaluación, calendario, precios o misiones del curso.

## Reproducir, comprobar y operar

```sh
python -m pip install -r discovery_labs/requirements-batch1.txt
python discovery_labs/scripts/prepare_fieldlab.py --case nasa-exoplanetas
python discovery_labs/scripts/run_fieldlab.py --case nasa-exoplanetas
python -m unittest discover -s discovery_labs/tests -v
python discovery_labs/tests/fieldlab_browser.py --case nasa-exoplanetas
python discovery_labs/scripts/agent_tools.py run --case nasa-exoplanetas --question D05-D1
```

La opción `--download` del preparador verifica bytes exactos del endpoint vivo y rechaza una revisión distinta sin sobrescribir el snapshot archivado. No se actualiza durante clase. Salida mediante staging, recibo verificable y cache por fuente/código/contratos/entorno. Red bloqueada al investigar; interfaz de agentes sin código arbitrario, 4 GiB de memoria, 50 s CPU, 60 s pared, 32 MiB por archivo y entorno sin tokens. El pipeline local tarda aproximadamente 3–4 segundos; no acredita duración de aula.

Cinco regresiones nuevas cubren referencias/flags, ausencia de imputación, errores firmados, universo fijo y reconciliación, contratos bloqueados y un proceso independiente desde el ZIP con otro PYTHONHASHSEED. Se comparan resultados, CSV y PNG exactos. Chromium: tres rutas × dos pantallas = seis combinaciones; catorce capturas, imágenes y enlaces locales comprobados, sin red, errores JS o overflow. CI añade ejecución y navegador de esta fuente a los pilotos existentes.

`DATA_READY` y tres rutas de investigación/visual/narrativa verificadas. `CLASS_READY` y `PUBLISHED` siguen cerradas. Tres rutas candidatas no equivalen a seis opciones listas ni a una clase aprobada.

## Progreso hasta este PR

| Dimensión | Lote 1 | Biblioteca |
| --- | --- | --- |
| Inventario | 7 candidatos conservados | 86/86 = 100% |
| Fuentes procesadas | 2/7 = 28.6% | 5/86 = 5.8% |
| Contratos específicos | 12/42 = 28.6% | 30/516 = 5.8% |
| Preguntas ejecutadas | 8/42 = 19.0% | 20/516 = 3.9% |
| Preguntas con figuras revisadas | 8/42 = 19.0% | 20/516 = 3.9%; 31 figuras distintas |
| Narrativas ejecutadas | 8/42 = 19.0% | 20/516 = 3.9% |
| Aprobación pedagógica | 0/7 | 0/86 |

No se declara terminado el Lote 1. Evidencias: `evidence/v3/fieldlab/nasa-exoplanetas/`. CI y revisión del commit remoto se registran en el PR, manteniéndolo en borrador.
