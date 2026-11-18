# El partido contado dos veces

Un pronóstico parece tener miles de observaciones. Antes de confiar en él, averigua qué significa una fila y qué información podía conocer antes del encuentro.

**Estado:** piloto técnico ejecutado y reproducible offline; NO listo para clase hasta ensayo humano de 45 minutos y revisión docente.

- [Alumno](ALUMNO.md) · [Cuaderno Python](alumno.ipynb) · [Docente](DOCENTE.md)
- [Snapshot](data/snapshot.csv) · [Procedencia, licencia y hash](data/manifest.json)

[Diccionario y unidades](DICCIONARIO.md).

## Elecciones disponibles

D10-D2 · victoria local por fase; D10-E · calibración del pronóstico y filas espejo.

Camino 1: comparar tasas de victoria local entre fases con conteos y sensibilidad por fecha. Camino 2: deduplicar por game_id, evaluar forecast previo y verificar Brier por perspectiva espejo. Contraste adversarial: contar filas como partidos y revisar elo_n.

## Reproducción

Desde la raíz del repositorio, con dependencias preparadas fuera de clase:

```bash
python discovery_labs/scripts/run_pilots.py --case nba-elo
```

Las tablas, el gráfico y results.json se crean en `discovery_labs/output/nba-elo/`; no hay descargas en ejecución. El snapshot es también la alternativa offline. Si falla el entorno, el dashboard contiene la evidencia calculada para discusión, con su alcance.

## Resultado comprobado

2,622 filas representan 1,311 partidos. En esta temporada histórica, la victoria local observada es 57.6%. El Brier del pronóstico previo es 0.20844 frente a 0.25 de una probabilidad constante de 0.5.

## Límites

Es una temporada histórica, incluidos playoffs. El bootstrap por fecha no elimina toda dependencia por equipos/series. La comparación por fase mezcla composición y selección de equipos. Marcadores y elo_n son posteriores y no son predictores permitidos.

Atribución: FiveThirtyEight, Historical NBA Elo; datos de encuentros atribuidos a Basketball-Reference en la documentación del productor.. CC BY 4.0. La licencia se aplica a datos, no a medios de terceros.
