# NASA Exoplanetas · candidato técnico

Snapshot público numérico de PS con default_flag=1 y descubrimientos hasta 2025. Derechos, referencias y condiciones: [data/RIGHTS.md](data/RIGHTS.md). Query, momento, bytes, hashes y conteo independiente: [data/manifest.json](data/manifest.json). No es una muestra aleatoria del universo ni un snapshot histórico de parámetros al cierre de 2025.

```sh
python -m pip install -r discovery_labs/requirements-batch1.txt
python discovery_labs/scripts/run_fieldlab.py --case nasa-exoplanetas
python discovery_labs/tests/fieldlab_browser.py --case nasa-exoplanetas
```

Tres rutas ejecutadas: C (agrupamientos), D1 (radio parecido a Tierra) y E (método/selección). A, B y D2 siguen bloqueadas. Se preparan siete figuras, móvil/proyección PNG/SVG, galería offline, guías, historias y screencast de 55 minutos. Los resultados de referencia y el ensayo pendiente se generan en teacher/, fuera del kit alumno. Las puertas de clase y publicación siguen cerradas.
