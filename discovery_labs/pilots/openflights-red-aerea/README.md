# El aeropuerto que parecía imprescindible

¿Qué significa importante en una red de aeropuertos: tener muchos destinos, conectar grupos o resistir un corte? Este caso usa una red histórica real para elegir una pregunta, criticar una métrica y defender una conclusión con límites.

**Estado:** cinco rutas técnicamente ejecutadas; no aprobado para clase. D16-A queda fuera de votación porque faltan demanda, precios y costos. Ensayo humano y revisión docente independiente no observados.

| ID | Investigación preparada |
| --- | --- |
| D16-B | Pérdida estructural de conectividad por país frente a retiros locales de referencia |
| D16-C | Comunidades y su estabilidad, con mapa y red agregada |
| D16-D1 | Grado frente a intermediación y sensibilidad de la aproximación |
| D16-D2 | Distancia geodésica frente a conexiones observadas y cambios de denominador |
| D16-E | Dirección, retiro de hubs y política de desacuerdos de metadata |

[Diccionario y unidades](DICCIONARIO.md) · [Procedencia y hashes](data/manifest.json) · [Licencia del productor](data/LICENSE) · [Contratos](../../contracts/batch1a.json).

Antes de clase, desde la raíz:

```sh
python -m pip install -r discovery_labs/requirements-batch1.txt
python discovery_labs/scripts/run_batch1.py --case openflights-red-aerea
python discovery_labs/scripts/agent_tools.py results --case openflights-red-aerea --question D16-D2
```

La salida está en `discovery_labs/output/v3/openflights-red-aerea/`. Abrir `student/index.html` para la contingencia sin conexión o entregar `student-offline.zip`, que incluye código ejecutable. Los guiones y referencias de facilitación están en `teacher/` y se generan por separado, fuera del ZIP de alumno y de los artefactos públicos de CI.

Para reproducir los bytes originales, fuera de clase:

```sh
python discovery_labs/scripts/prepare_openflights.py --download
```

La ingesta valida todos los hashes antes de reemplazar archivos. La investigación no usa red ni credenciales. Ningún conteo representa vuelos o pasajeros; el productor informa que las rutas dejaron de actualizarse en junio de 2014. No usar para navegación ni como descripción de conectividad actual.
