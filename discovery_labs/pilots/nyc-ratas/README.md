# NYC Rodent Inspections · candidato técnico

Una ventana cerrada de 2024, seis campos y datos públicos del productor NYC DOHMH / NYC Open Data. [Manifiesto](data/manifest.json), [derechos y límites](data/RIGHTS.md), [diccionario](DICCIONARIO.md).

```sh
python -m pip install -r discovery_labs/requirements-batch1.txt
python discovery_labs/scripts/run_fieldlab.py --case nyc-ratas
python discovery_labs/tests/fieldlab_browser.py --case nyc-ratas
```

Cuatro rutas ejecutadas: B acotada explícitamente a boroughs y predios inspeccionados, C temporal/geográfica, D1 contraste estacional2024 y E auditoría de denominadores. A y D2 bloqueadas. No se estima población de roedores. El kit offline ofrece siete figuras en móvil/proyección, tablas y motor. El guion y las referencias docentes permanecen fuera del paquete alumno; ensayo y aprobación pendientes.
