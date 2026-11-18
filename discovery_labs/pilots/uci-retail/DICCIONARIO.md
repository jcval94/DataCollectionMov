# Diccionario del snapshot retail

Unidad: línea de factura, no cesta ni cliente. Todas las filas de cada factura seleccionada se conservan. Periodo: noviembre de 2011, según InvoiceDate del archivo. La zona horaria no se ha verificado; no usar para comparaciones entre husos.

| Campo | Significado y control |
| --- | --- |
| InvoiceNo | Identificador de factura como texto; puede repetirse en varias líneas. Prefijo C señala cancelación según UCI, sin garantizar emparejamiento con venta original. |
| StockCode | Código de producto como texto. La política de análisis acepta cinco dígitos con letras opcionales; los demás se excluyen de ese ranking, conservándose en el original. |
| Quantity | Unidades firmadas por línea; negativo puede representar crédito/ajuste registrado. No equivale a compra físicamente devuelta y enlazada. |
| InvoiceDate | Fecha/hora sin zona verificada, normalizada a formato ISO para este snapshot. |
| UnitPrice | Precio unitario en GBP según UCI. No es costo ni margen. Los precios no positivos quedan fuera del análisis económico definido. |
| Country | País declarado en el registro, no residencia verificada de cada persona. |
| customer_id_missing | 1 si CustomerID estaba vacío en el original; 0 en otro caso. El ID de cliente se retiró. No permite reconstruir perfiles de personas. |

Bruto positivo: suma de max(Quantity × UnitPrice, 0). Créditos: suma del valor absoluto de importes negativos. Neto firmado: bruto menos créditos. Los duplicados exactos se conservan y se eliminan únicamente en una sensibilidad separada. Los empates de ranking se ordenan por código; cambiar puesto no implica siempre un cambio económico grande.

Las descripciones se retiraron junto con CustomerID. Las relaciones de cesta usan factura; relaciones de cliente están bloqueadas en este snapshot. Fuente, atribución, selección y hash: data/manifest.json.
