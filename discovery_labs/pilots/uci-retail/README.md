# La venta que cambió de puesto

Una tienda quiere destacar sus productos estrella. ¿Lo que más factura sigue siendo lo que más deja al registrar créditos?

**Estado:** piloto técnico ejecutado y reproducible offline; NO listo para clase hasta ensayo humano de 45 minutos y revisión docente.

- [Alumno](ALUMNO.md) · [Cuaderno Python](alumno.ipynb) · [Docente](DOCENTE.md)
- [Snapshot](data/snapshot.csv) · [Procedencia, licencia y hash](data/manifest.json)

## Elecciones disponibles

D31-A · neto por producto; D31-E · ranking bruto/neto; D31-B · líneas frente a facturas sin ID.

Camino 1: sumar importes firmados por producto mediante groupby. Camino 2: reconstruir bruto menos créditos con un acumulador Decimal independiente. Sensibilidad: repetir sin duplicados y contar faltantes por línea/factura.

## Reproducción

Desde la raíz del repositorio, con dependencias preparadas fuera de clase:

```bash
python discovery_labs/scripts/run_pilots.py --case uci-retail
```

Las tablas, el gráfico y results.json se crean en `discovery_labs/output/uci-retail/`; no hay descargas en ejecución. El snapshot es también la alternativa offline. Si falla el entorno, el dashboard contiene la evidencia calculada para discusión, con su alcance.

## Resultado comprobado

En 300 facturas de noviembre de 2011: bruto 95,755.66 GBP, créditos 4,426.64 GBP y neto firmado 91,329.02 GBP. 1,875 productos cambian de posición; 30.1% de líneas y 12.7% de facturas carecen de ID de cliente.

## Límites

La muestra se seleccionó por factura, no por cliente; una nota negativa no está emparejada con su venta original. No hay costos para calcular utilidad. No inferir perfil social de clientes a partir de un ID ausente.

Atribución: Chen, D. (2015), Online Retail, UCI, doi:10.24432/C5BW33. CC BY 4.0. La licencia se aplica a datos, no a medios de terceros.
