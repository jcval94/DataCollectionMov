# Despliegue en Google Apps Script

Esta carpeta contiene todo lo necesario para publicar la web app.

## Opcion con clasp

1. Instalar y autenticar `clasp`.

```powershell
npm install -g @google/clasp
clasp login
```

2. Crear el proyecto o vincular uno existente.

```powershell
cd SubRepo/appscript
clasp create --type webapp --title "Rutas de atencion por incidente"
```

Si ya tienes un proyecto Apps Script, crea `.clasp.json` con:

```json
{
  "scriptId": "TU_SCRIPT_ID",
  "rootDir": "."
}
```

3. Subir y desplegar.

```powershell
clasp push
clasp deploy --description "Rutas de atencion por incidente"
```

## Configuracion

No se requiere exponer `GOOGLE_MAPS_API_KEY` al cliente. El mapa se renderiza con Leaflet/OpenStreetMap y la ruta vial por codigo postal usa el servicio server-side `Maps.DirectionFinder` de Apps Script.

Si `Maps.DirectionFinder` falla por cuota o limite de puntos, la app mantiene el trazado por centroides coloreado por volumen de eventos.
