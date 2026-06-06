# SubRepo - Rutas de atencion por incidentes

Subrepositorio autocontenido para regenerar datos de rutas y desplegar una web app ligera en Google Apps Script.

## Estructura

- `data/`: insumos mínimos cacheados para reproducir la app.
- `scripts/build_routes.py`: generador de rutas/GeoJSON/HTML de análisis con Google Routes API.
- `scripts/build_appscript_data.py`: empaqueta datos compactos para Apps Script.
- `appscript/`: proyecto listo para copiar o subir con `clasp`.

## Regenerar datos compactos

```powershell
cd SubRepo
python -m pip install -r requirements.txt
$env:GOOGLE_MAPS_API_KEY = [Environment]::GetEnvironmentVariable('GOOGLE_MAPS_API_KEY','Machine')
python scripts/build_appscript_data.py
```

El despliegue en Apps Script usa `appscript/Code.gs`, `appscript/Data.gs`, `appscript/Index.html` y `appscript/appsscript.json`.

## Apps Script

La app usa Leaflet y datos compactos. El selector principal incluye:

- Escenario bomberos / proteccion civil
- Salud / emergencia medica 19 rutas, 13,472 eventos
- Seguridad / vigilancia 61 rutas, 26,504 eventos

En Seguridad se habilita un selector de codigo postal. Para cada CP, la app dibuja la secuencia de centroides coloreada por volumen de eventos y solicita a Apps Script una ruta vial con `Maps.DirectionFinder`; si falla por cuota o limite de waypoints, conserva el trazado por centroides.
