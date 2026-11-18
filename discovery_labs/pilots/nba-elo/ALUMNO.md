# El partido contado dos veces

Un pronóstico parece tener miles de observaciones. Antes de confiar en él, averigua qué significa una fila y qué información podía conocer antes del encuentro.

**Votación:** D10-D2 · victoria local por fase; D10-E · calibración del pronóstico y filas espejo.

**Concepto:** Unidad independiente, calibración y fuga de información.

Camino 1: comparar tasas de victoria local entre fases con conteos y sensibilidad por fecha. Camino 2: deduplicar por game_id, evaluar forecast previo y verificar Brier por perspectiva espejo. Contraste adversarial: contar filas como partidos y revisar elo_n.

Campos mínimos: game_id, team_id, _iscopy, date_game, game_location, forecast, elo_i, elo_n, pts, opp_pts, is_playoffs.

Lee [el registro de investigación](../../templates/ALUMNO.md), completa tu predicción y abre [el cuaderno](alumno.ipynb). No mires resultados antes de apostar.

Si reinicias sesión, vuelve a correr desde el principio. Para trabajar offline, usa data/snapshot.csv y el script de la carpeta scripts.
