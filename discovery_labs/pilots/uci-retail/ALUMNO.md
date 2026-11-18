# La venta que cambió de puesto

Una tienda quiere destacar sus productos estrella. ¿Lo que más factura sigue siendo lo que más deja al registrar créditos?

**Votación:** D31-A · neto por producto; D31-E · ranking bruto/neto; D31-B · líneas frente a facturas sin ID.

**Concepto:** Denominadores y definiciones de una métrica económica.

Camino 1: sumar importes firmados por producto mediante groupby. Camino 2: reconstruir bruto menos créditos con un acumulador Decimal independiente. Sensibilidad: repetir sin duplicados y contar faltantes por línea/factura.

Campos mínimos: InvoiceNo, StockCode, Quantity, UnitPrice, InvoiceDate, Country, customer_id_missing.

Lee [el registro de investigación](../../templates/ALUMNO.md), completa tu predicción y abre [el cuaderno](alumno.ipynb). No mires resultados antes de apostar.

Si reinicias sesión, vuelve a correr desde el principio. Para trabajar offline, usa data/snapshot.csv y el script de la carpeta scripts.
