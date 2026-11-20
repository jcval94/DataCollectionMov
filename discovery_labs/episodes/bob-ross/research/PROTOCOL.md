# O1 · protocolo exploratorio fijado antes de la ejecución

Fecha de decisión: 19 de noviembre de 2026, America/Mexico_City. No es preregistro independiente: ya conocemos los conteos históricos y el k-medoids de cuatro salas. No se afirma prioridad mundial. La novedad potencial es el contraste secuencial condicionado y la robustez reproducible, no volver a descubrir árboles o agrupamientos.

## Puerta de datos

`audit.py` debe pasar antes de cualquier cálculo. Usar el CSV inmutable de FiveThirtyEight/Walt Hickey, CC BY 4.0, SHA `42045c8b8aaa8296095d6b294927fb9d0f73a57259f59b560c375844c0fe01cf`. Ninguna imagen, audio o transcripción se descarga. Conservar íntegros los tres informes recibidos y contrastar su MANIFEST. Análisis ejecutables offline con Python ≥3.11, biblioteca estándar; semilla 20261119.

## BR-14 / H8 · secuencia ordinal

**Cómo:** cuatro motivos fijados por H8: OCEAN, OVAL_FRAME, WINTER y CABIN. Modelo M14: tablas Markov de orden 1, P(1|1) y P(1|0), sin afirmar ajuste causal ni predicción fuera de muestra. Contraste independiente: 10,000 permutaciones del orden de episodios dentro de cada temporada; se mueve el vector completo de etiquetas para preservar coocurrencias y totales. Estadístico: número de transiciones 1→1. H0: intercambiabilidad intratemporada; alternativa unilateral: menos repeticiones. Esperanza exacta por temporada con n=13 y k positivos: k(k−1)/n. Holm sobre cuatro pruebas primarias; alfa .05, razón observado/esperado <.7 según H8. Banda predictiva nula 95% y error Monte Carlo, no IC del efecto. Reportar también cola superior exploratoria para distinguir rachas de inhibición.

Población primaria: los 403 episodios, 372 transiciones. Sensibilidad: anfitrión sin puentear huecos ni temporadas; reordenar solo etiquetas de anfitrión en sus posiciones originales (las de invitados permanecen fijas). Segunda sensibilidad: excluir las tres filas vacías, manteniendo posiciones y huecos. No convertir vecinos tras filtrar en adyacencias reales. No cruzar temporadas. Reportar límites de potencia y todas las pruebas, incluidas nulas.

**Por qué:** alternancia y rachas no son iguales a baja prevalencia. El nulo condicionado evita confundir rareza de un tema con programación deliberada; grabación por bloques sigue siendo rival sin logs.

**Para qué:** enseñar diseño de un nulo apropiado y decidir si vale la pena recuperar cronología. No afirmar intención editorial ni memoria psicológica.

## BR-07 / H3 y H9 · asociaciones

**Cómo:** M10, baseline de independencia y lift sobre las 12 familias existentes, 66 pares en 381 episodios GUEST=0. Fisher bilateral exacto, BH sobre los 66; tabla completa 2×2, OR (null si denominador cero, sin pseudoconteo escondido). Excluir de la lista de candidatos interpretativos `montanas–nieve`, solapadas por SNOWY_MOUNTAIN, pero conservar la fila y su prueba en el universo BH. Contraste secundario previamente fijado: CABIN–WINTER, Fisher y 10,000 permutaciones de WINTER dentro de temporada; no presentarlo como independiente de su selección por DR-03. Intervalo bootstrap por 31 temporadas de lift, 2,000 réplicas, sin selección de pares por p. Es sensibilidad al conjunto de temporadas observado, no error muestral de un censo. H3 queda solo parcialmente cubierta: no se modela tiempo, ni número de objetos, ni se prueba la restricción de 26 minutos.

**Por qué:** una coocurrencia puede depender de las prevalencias, una jerarquía del diccionario o mezcla de temporadas. Las 12 familias son una transformación explícita, no motivos físicamente independientes.

**Para qué:** enseñar denominadores, corrección múltiple y diferencia entre asociación y mecanismo. Toda asociación detectada permanece exploratoria.

## BR-09 / H6 · agrupamiento y sensibilidad

**Cómo:** M07, reutilizar k-medoids determinista sobre 12 familias en 381 episodios. k=2…6 como diagnóstico, sin seleccionar un «k verdadero». Comparar k=4 con Euclídea y con Jaccard sin árboles. Contraste independiente: 2,000 bootstrap por temporadas del ARI entre las dos particiones completas, con IC percentil. Es incertidumbre de acuerdo condicional a particiones fijas, **no** estabilidad de modelos reajustados. Guardar asignaciones por episodio, medoids, tamaños y silhouette. Sensibilidad adicional: excluir las tres filas sin etiquetas y reajustar k=4. No comparar silhouettes de espacios distintos como una escala común.

**Por qué:** la división puede depender de la ontología y de una elección operativa de cuatro salas. Medir desacuerdo sirve para refutar la lectura de estilos únicos.

**Para qué:** mostrar qué responde realmente un algoritmo. H6 híbrida/KMeans/Bernoulli, bootstrap con reajuste y validación visual siguen pendientes; este O1 es parcial y no valida una taxonomía artística.

## Decisiones progresivas

Tras guardar resultados, realizar DR-05a acotada a las fuentes contrastadas y O1 ejecutadas; dejar pendientes explícitas las fuentes no verificadas. No activar O2 si solo se cumple un umbral nominal sin robustez o falta una fuente central. No activar O3 sin O2 medida. DR-04 profundo y DR-05b quedan diferidos. Ningún resultado es APPROVED sin aprobación humana. El HTML conserva las 14 investigaciones en un solo índice y muestra solo O1.
