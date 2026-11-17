# Guion · La venta que cambió de puesto

Seguir [la secuencia de 45 minutos](../../templates/DOCENTE.md).

## Preparación

Concepto principal: Denominadores y definiciones de una métrica económica. Audiencia: principiantes con IA copiloto; actividad opcional, sin evaluación formal. Comprueba 7293 filas, 7 columnas, 414,094 bytes y SHA256 `f3c895e068c4267a24aafb5ab097b03105a4376fab87028647841fe5eaeae8bc`.

## Elección real

D31-A · neto por producto; D31-E · ranking bruto/neto; D31-B · líneas frente a facturas sin ID.

Camino 1: sumar importes firmados por producto mediante groupby. Camino 2: reconstruir bruto menos créditos con un acumulador Decimal independiente. Sensibilidad: repetir sin duplicados y contar faltantes por línea/factura.

## Evidencia de referencia, después de la predicción

En 300 facturas de noviembre de 2011: bruto 95,755.66 GBP, créditos 4,426.64 GBP y neto firmado 91,329.02 GBP. 1,875 productos cambian de posición; 30.1% de líneas y 12.7% de facturas carecen de ID de cliente.

La muestra se seleccionó por factura, no por cliente; una nota negativa no está emparejada con su venta original. No hay costos para calcular utilidad. No inferir perfil social de clientes a partir de un ID ausente.

Pedir dos comprobaciones independientes, permitir una objeción explícita a la IA y cerrar con decisión humana. No llamar rentable al neto, muestra independiente a una fila espejo ni natural a un grupo impuesto.

## Ensayo

Estado: PENDIENTE. Se necesita la sesión humana observada, no más tiempo de CPU. Registrar intervalos, incidentes, ruta elegida y cierre, según la plantilla.
