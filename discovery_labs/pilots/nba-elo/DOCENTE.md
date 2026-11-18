# Guion · El partido contado dos veces

Seguir [la secuencia de 45 minutos](../../templates/DOCENTE.md).

## Preparación

Concepto principal: Unidad independiente, calibración y fuga de información. Audiencia: principiantes con IA copiloto; actividad opcional, sin evaluación formal. Comprueba 2622 filas, 23 columnas, 369,469 bytes y SHA256 `c960cfbeca7b5449ea675b64421b99b224047fbc898eccd56113ef344a9ca6e2`.

## Elección real

D10-D2 · victoria local por fase; D10-E · calibración del pronóstico y filas espejo.

Camino 1: comparar tasas de victoria local entre fases con conteos y sensibilidad por fecha. Camino 2: deduplicar por game_id, evaluar forecast previo y verificar Brier por perspectiva espejo. Contraste adversarial: contar filas como partidos y revisar elo_n.

## Evidencia de referencia, después de la predicción

2,622 filas representan 1,311 partidos. En esta temporada histórica, la victoria local observada es 57.6%. El Brier del pronóstico previo es 0.20844 frente a 0.25 de una probabilidad constante de 0.5.

Es una temporada histórica, incluidos playoffs. El bootstrap por fecha no elimina toda dependencia por equipos/series. La comparación por fase mezcla composición y selección de equipos. Marcadores y elo_n son posteriores y no son predictores permitidos.

Pedir dos comprobaciones independientes, permitir una objeción explícita a la IA y cerrar con decisión humana. No llamar rentable al neto, muestra independiente a una fila espejo ni natural a un grupo impuesto.

## Ensayo

Estado: PENDIENTE. Se necesita la sesión humana observada, no más tiempo de CPU. Registrar intervalos, incidentes, ruta elegida y cierre, según la plantilla.
