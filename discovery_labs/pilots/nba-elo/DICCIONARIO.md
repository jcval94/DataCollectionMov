# Diccionario del snapshot NBA

Unidad original: equipo-partido, normalmente dos filas por game_id. Selección: NBA, year_id=2015 (temporada 2014–2015), incluidos playoffs. No describe la liga actual. El análisis de calibración conserva una fila por partido, y el de localía usa únicamente game_location=H.

| Campo utilizado | Significado y control |
| --- | --- |
| game_id | ID de partido; deben existir dos filas de equipos distintos en el snapshot original. |
| team_id / opp_id | Equipo y rival de la fila. Los cambios de identidad histórica se estudian con fran_id y documentación externa. |
| _iscopy | Marca del productor para filas espejo. La ruta de calibración usa _iscopy=0 y comprueba unicidad por game_id. |
| year_id / lg_id | Año de temporada y liga; se filtran de forma explícita antes de construir el snapshot. |
| date_game | Fecha declarada del partido. Se usa como bloque de sensibilidad, sin afirmar independencia completa entre fechas. |
| game_location | H local, A visitante o N neutral según el contrato del productor. El análisis local no mezcla neutral con visitante. |
| is_playoffs | Indicador de fase. La selección a playoffs cambia la composición de equipos; comparar fases no identifica el efecto causal de la localía. |
| forecast | Probabilidad previa de victoria para el equipo de la fila. La suma de ambas perspectivas debe ser aproximadamente 1. |
| elo_i | Rating Elo antes del partido. |
| elo_n | Rating posterior al partido. Prohibido como predictor de ese mismo resultado. |
| pts / opp_pts | Marcadores, usados para construir la etiqueta de victoria. Son posteriores; prohibidos como features previas. |

El CSV conserva las 23 columnas del original; el código emplea únicamente el contrato descrito para este piloto. Las demás se conservan para trazabilidad, sin atribuirles un uso analítico no comprobado. No hay salarios ni datos de fichajes suficientes para responder D10-A. Brier = promedio de (forecast − victoria)² por partido único; menor es mejor. La base 0.5 tiene Brier 0.25 para una etiqueta binaria. El bootstrap por fecha es una sensibilidad exploratoria, no una garantía de independencia por equipos y series.

Fuente, edición y hash: data/manifest.json. Diccionario original: https://github.com/fivethirtyeight/data/blob/master/nba-elo/README.md; fijar commit antes de reutilizarlo como fuente de un cuaderno del curso.
