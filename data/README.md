# Lectura de datos

Este directorio se llena automaticamente por GitHub Actions.

| Carpeta | Contenido |
| --- | --- |
| `current/` | Ultimo CSV de cada tabla. |
| `history/<tabla>/` | Snapshots historicos de esa tabla. |
| `manifests/` | JSON de control por corrida. |
| `artifacts/current/` | Ultimo HTML por mapa/artefacto visual. |
| `artifacts/history/<artefacto>/` | Historico de HTMLs. |

Ejemplo:

```python
from pathlib import Path
import pandas as pd

actual = pd.read_csv("data/current/tomtom_cdmx_flow.csv")
historico = pd.concat(
    (pd.read_csv(path) for path in sorted(Path("data/history/tomtom_cdmx_flow").glob("*.csv"))),
    ignore_index=True,
)
```

La guia completa esta en `../docs/README_LECTURA_TABLAS.md`.
