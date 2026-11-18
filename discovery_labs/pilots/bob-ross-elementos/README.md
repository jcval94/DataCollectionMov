# Los árboles que faltaban

La intuición dice que todos sus cuadros tienen árboles. ¿Basta mirar algunos ejemplos? Después intenta organizar una exposición en cuatro salas y cuestiona tus propios grupos.

**Estado:** piloto técnico ejecutado y reproducible offline; NO listo para clase hasta ensayo humano de 45 minutos y revisión docente.

- [Alumno](ALUMNO.md) · [Cuaderno Python](alumno.ipynb) · [Docente](DOCENTE.md)
- [Snapshot](data/snapshot.csv) · [Procedencia, licencia y hash](data/manifest.json)

[Diccionario y unidades](DICCIONARIO.md).

## Elecciones disponibles

D85-D1 · árboles; D85-D2 · montañas y nieve; D85-C · grupos de motivos; D85-B · invitados frente al anfitrión.

Camino 1: tabla de frecuencias y contraejemplos, incluyendo/excluyendo invitados. Camino 2: clustering jerárquico con Jaccard y contraste con Euclídea; excluir siempre identificador y temporada como features.

## Reproducción

Desde la raíz del repositorio, con dependencias preparadas fuera de clase:

```bash
python discovery_labs/scripts/run_pilots.py --case bob-ross-elementos
```

Las tablas, el gráfico y results.json se crean en `discovery_labs/output/bob-ross-elementos/`; no hay descargas en ejecución. El snapshot es también la alternativa offline. Si falla el entorno, el dashboard contiene la evidencia calculada para discusión, con su alcance.

## Resultado comprobado

Entre 381 episodios del anfitrión hay 36 sin TREE ni TREES registrados. El clustering propuesto cambia fuertemente al pasar de Jaccard a Euclídea: ARI −0.0458. La etiqueta de un motivo no describe píxeles ni su cantidad.

## Límites

Se analizan etiquetas humanas de episodios, no todas las pinturas. Cuatro grupos es una restricción narrativa, no un número descubierto de estilos naturales. La discrepancia de agrupamientos es un resultado que debe mostrarse.

Atribución: Walt Hickey / FiveThirtyEight, elementos por episodio de The Joy of Painting; CC BY 4.0 sólo para las etiquetas.. CC BY 4.0. La licencia se aplica a datos, no a medios de terceros.
