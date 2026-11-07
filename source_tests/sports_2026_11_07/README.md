# Tests de fuentes: resultados, registros e imágenes

**6 fuentes comprobadas.** Fechas de las peticiones conservadas en este informe: `2026-11-07T06:03:55+00:00` a `2026-11-07T06:03:58+00:00` (UTC).

Este README contiene las pruebas y sus ejemplos. Las tablas proceden de respuestas reales; los errores quedan visibles. Las imágenes tienen una prueba adicional de descarga completa y decodificación. Cada capa conserva su propia fecha: añadir una imagen no equivale a volver a probar toda la fuente.

| Resultado más útil por fuente | Fuentes |
| --- | ---: |
| `DATA_SAMPLE` — Registros recuperados | 6 |

Una página `DOC_ONLY` no acredita registros descargados. `METADATA_SAMPLE` sólo acredita metadatos. `CACHED_SAMPLE` usa archivos del repo. Una muestra por prefijo no es aleatoria ni prueba calidad global; su hash no identifica el archivo completo.

Los errores/bloqueos describen estas peticiones desde este entorno, sin afirmar que el proveedor esté caído globalmente. No se inventan registros para sustituir datos inaccesibles.


## Índice de tests

| Fuente | Resultado |
| --- | --- |
| [pgnmentor-ajedrez](#pgnmentor-ajedrez) | `DATA_SAMPLE` |
| [statsbomb-futbol](#statsbomb-futbol) | `DATA_SAMPLE` |
| [cross-tables-scrabble](#cross-tables-scrabble) | `DATA_SAMPLE` |
| [nba-elo](#nba-elo) | `DATA_SAMPLE` |
| [jolpica-f1](#jolpica-f1) | `DATA_SAMPLE` |
| [opendota-partidas](#opendota-partidas) | `DATA_SAMPLE` |

## Reproducir

Desde la raíz del repositorio:

```bash
python -m pip install pypdf openpyxl Pillow
# Rehacer sólo los README a partir de la evidencia guardada (sin red):
python scripts/render_source_readmes.py
# Probar de nuevo las imágenes y actualizar los README:
python scripts/check_visual_examples.py
python scripts/render_source_readmes.py
# Nueva prueba de acceso a todas las fuentes:
python scripts/probe_catalog_sources.py
# O sólo algunas, en selected/ para conservar el informe acumulado:
python scripts/probe_catalog_sources.py --only dof-publicaciones bob-ross-paletas
```

`pypdf` y `openpyxl` son opcionales para PDF/XLSX; `Pillow` se usa para decodificar imágenes. El verificador de imágenes devuelve 1 si falla una imagen. En el verificador de fuentes, el código 0 sin `--strict` significa informe generado; `--strict` devuelve 1 si falla alguna comprobación, incluidos medios enlazados. No usa credenciales personales ni activa recolección programada.

## Tests y ejemplos por fuente

### pgnmentor-ajedrez

**Ajedrez: grandes maestros, campeonatos y aperturas en PGN** — `DATA_SAMPLE`.

Ampliación de deportes y juegos: pruebas acotadas de notación o registros reales; las tres preguntas son propuestas de investigación, sin hallazgos calculados.

**Prueba 1: `DATA_SAMPLE`** · [pgn](https://www.pgnmentor.com/events/WorldChamp2021.pgn) · HTTP `200`.

Captura UTC: `2026-11-07T06:03:55+00:00`; duración: 3.593 s.

Cabeceras y fragmentos de jugadas de las dos primeras partidas del PGN; no se validó la legalidad de movimientos ni el corpus completo. El archivo por jugador puede incluir etapas anteriores a su título GM.

Contenido: `application/x-chess-pgn`; 8,438 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| Event | WCh 2021 | WCh 2021 |
| Site | Dubai UAE | Dubai UAE |
| Date | 2021.11.26 | 2021.11.27 |
| Round | 1 | 2 |
| White | Nepomniachtchi,I | Carlsen,M |
| Black | Carlsen,M | Nepomniachtchi,I |
| Result | 1/2-1/2 | 1/2-1/2 |
| WhiteElo | 2782 | 2855 |
| BlackElo | 2855 | 2782 |
| ECO | C88 | E06 |
| moves_excerpt | 1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Ba4 Nf6 5.O-O Be7 6.Re1 b5 7.Bb3 O-O 8.h3 Na5 9.Nxe5 Nxb3 10.axb3 Bb7 11.d3 d5 12.exd5 Qxd5 13.Qf3 Bd6 14.Kf1 Rfb8 15.Qxd5 Nxd5 16.Bd2 c5 17.Nf3 Rd8 18… | 1.d4 Nf6 2.c4 e6 3.Nf3 d5 4.g3 Be7 5.Bg2 O-O 6.O-O dxc4 7.Qc2 b5 8.Ne5 c6 9.a4 Nd5 10.Nc3 f6 11.Nf3 Qd7 12.e4 Nb4 13.Qe2 Nd3 14.e5 Bb7 15.exf6 Bxf6 16.Ne4 Na6 17.Ne5 Bxe5 18.dxe5 N… |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "Event": "WCh 2021",
    "Site": "Dubai UAE",
    "Date": "2021.11.26",
    "Round": "1",
    "White": "Nepomniachtchi,I",
    "Black": "Carlsen,M",
    "Result": "1/2-1/2",
    "WhiteElo": "2782",
    "BlackElo": "2855",
    "ECO": "C88",
    "moves_excerpt": "1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Ba4 Nf6 5.O-O Be7 6.Re1 b5 7.Bb3 O-O 8.h3 Na5 9.Nxe5 Nxb3 10.axb3 Bb7 11.d3 d5 12.exd5 Qxd5 13.Qf3 Bd6 14.Kf1 Rfb8 15.Qxd5 Nxd5 16.Bd2 c5 17.Nf3 Rd8 18…"
  },
  {
    "Event": "WCh 2021",
    "Site": "Dubai UAE",
    "Date": "2021.11.27",
    "Round": "2",
    "White": "Carlsen,M",
    "Black": "Nepomniachtchi,I",
    "Result": "1/2-1/2",
    "WhiteElo": "2855",
    "BlackElo": "2782",
    "ECO": "E06",
    "moves_excerpt": "1.d4 Nf6 2.c4 e6 3.Nf3 d5 4.g3 Be7 5.Bg2 O-O 6.O-O dxc4 7.Qc2 b5 8.Ne5 c6 9.a4 Nd5 10.Nc3 f6 11.Nf3 Qd7 12.e4 Nb4 13.Qe2 Nd3 14.e5 Bb7 15.exf6 Bxf6 16.Ne4 Na6 17.Ne5 Bxe5 18.dxe5 N…"
  }
]
```

</details>

**Prueba 2: `DATA_SAMPLE`** · [pgn_zip](https://www.pgnmentor.com/players/Carlsen.zip) · HTTP `200`.

Captura UTC: `2026-11-07T06:03:58+00:00`; duración: 3.319 s.

Cabeceras y fragmentos de jugadas de las dos primeras partidas del PGN; no se validó la legalidad de movimientos ni el corpus completo. El archivo por jugador puede incluir etapas anteriores a su título GM.

Contenido: `application/zip`; 1,849,084 bytes leídos; alcance del hash: `complete_response`.

Miembro del ZIP: `Carlsen.pgn`; 65,536 bytes leídos de 5,732,853 declarados. SHA-256 `8983c98e1d3aab0f8bae7a421b64546dfd3aa268f6c5a54d068821851a5cd132`; alcance `member_prefix`. Se leyó dentro del archivo, sin extraer rutas al disco.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| Event | Troll Masters | Troll Masters |
| Site | Gausdal NOR | Gausdal NOR |
| Date | 2001.01.05 | 2001.01.06 |
| Round | 1 | 2 |
| White | Edvardsen,R | Carlsen,Magnus |
| Black | Carlsen,Magnus | Brameld,A |
| Result | 1/2-1/2 | 0-1 |
| WhiteElo | 2055 |  |
| BlackElo |  | 2095 |
| ECO | D12 | B05 |
| moves_excerpt | 1.d4 Nf6 2.Nf3 d5 3.e3 Bf5 4.c4 c6 5.Nc3 e6 6.Bd3 Bxd3 7.Qxd3 Nbd7 8.b3 Bd6 9.O-O O-O 10.Bb2 Qe7 11.Rad1 Rad8 12.Rfe1 dxc4 13.bxc4 e5 14.dxe5 Nxe5 15.Nxe5 Bxe5 16.Qe2 Rxd1 17.Rxd1 … | 1.e4 Nf6 2.e5 Nd5 3.d4 d6 4.Nf3 Bg4 5.Bc4 e6 6.O-O Nb6 7.Be2 Be7 8.h3 Bh5 9.Bf4 Nc6 10.c3 O-O 11.Nbd2 d5 12.b4 a5 13.a3 Qd7 14.Qc2 Bg6 15.Bd3 Rfc8 16.Rfb1 Bf8 17.h4 Ne7 18.g3 Qa4 1… |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "Event": "Troll Masters",
    "Site": "Gausdal NOR",
    "Date": "2001.01.05",
    "Round": "1",
    "White": "Edvardsen,R",
    "Black": "Carlsen,Magnus",
    "Result": "1/2-1/2",
    "WhiteElo": "2055",
    "BlackElo": "",
    "ECO": "D12",
    "moves_excerpt": "1.d4 Nf6 2.Nf3 d5 3.e3 Bf5 4.c4 c6 5.Nc3 e6 6.Bd3 Bxd3 7.Qxd3 Nbd7 8.b3 Bd6 9.O-O O-O 10.Bb2 Qe7 11.Rad1 Rad8 12.Rfe1 dxc4 13.bxc4 e5 14.dxe5 Nxe5 15.Nxe5 Bxe5 16.Qe2 Rxd1 17.Rxd1 …"
  },
  {
    "Event": "Troll Masters",
    "Site": "Gausdal NOR",
    "Date": "2001.01.06",
    "Round": "2",
    "White": "Carlsen,Magnus",
    "Black": "Brameld,A",
    "Result": "0-1",
    "WhiteElo": "",
    "BlackElo": "2095",
    "ECO": "B05",
    "moves_excerpt": "1.e4 Nf6 2.e5 Nd5 3.d4 d6 4.Nf3 Bg4 5.Bc4 e6 6.O-O Nb6 7.Be2 Be7 8.h3 Bh5 9.Bf4 Nc6 10.c3 O-O 11.Nbd2 d5 12.b4 a5 13.a3 Qd7 14.Qc2 Bg6 15.Bd3 Rfc8 16.Rfb1 Bf8 17.h4 Ne7 18.g3 Qa4 1…"
  }
]
```

</details>

### statsbomb-futbol

**Fútbol soccer: partidos, eventos y xG de StatsBomb Open Data** — `DATA_SAMPLE`.

Ampliación de deportes y juegos: pruebas acotadas de notación o registros reales; las tres preguntas son propuestas de investigación, sin hallazgos calculados.

**Prueba 1: `DATA_SAMPLE`** · [json](https://raw.githubusercontent.com/hudl/open-data/master/data/matches/43/106.json) · HTTP `200`.

Captura UTC: `2026-11-07T06:03:55+00:00`; duración: 3.394 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

Contenido: `text/plain; charset=utf-8`; 119,132 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| match_id | 3857276 | 3857271 |
| match_date | 2022-12-01 | 2022-11-21 |
| home_team.home_team_name | Canada | England |
| away_team.away_team_name | Morocco | Iran |
| home_score | 1 | 6 |
| away_score | 2 | 2 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "match_id": 3857276,
    "match_date": "2022-12-01",
    "home_team.home_team_name": "Canada",
    "away_team.away_team_name": "Morocco",
    "home_score": 1,
    "away_score": 2
  },
  {
    "match_id": 3857271,
    "match_date": "2022-11-21",
    "home_team.home_team_name": "England",
    "away_team.away_team_name": "Iran",
    "home_score": 6,
    "away_score": 2
  }
]
```

</details>

**Prueba 2: `DATA_SAMPLE`** · [json](https://raw.githubusercontent.com/hudl/open-data/master/data/events/3857276.json) · HTTP `200`.

Captura UTC: `2026-11-07T06:03:58+00:00`; duración: 3.186 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

Contenido: `text/plain; charset=utf-8`; 2,811,450 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| id | 1f60fe1e-0340-49e2-975e-f16f54c5da1a | d5ffdab0-a19a-497e-a0f6-d5403bfcc2b5 |
| index | 1 | 2 |
| period | 1 | 1 |
| timestamp | 00:00:00.000 | 00:00:00.000 |
| type.name | Starting XI | Starting XI |
| team.name | Canada | Morocco |
| tactics.formation | 4411 | 433 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "id": "1f60fe1e-0340-49e2-975e-f16f54c5da1a",
    "index": 1,
    "period": 1,
    "timestamp": "00:00:00.000",
    "type.name": "Starting XI",
    "team.name": "Canada",
    "tactics.formation": 4411
  },
  {
    "id": "d5ffdab0-a19a-497e-a0f6-d5403bfcc2b5",
    "index": 2,
    "period": 1,
    "timestamp": "00:00:00.000",
    "type.name": "Starting XI",
    "team.name": "Morocco",
    "tactics.formation": 433
  }
]
```

</details>

### cross-tables-scrabble

**Scrabble: partidas anotadas y turnos en GCG** — `DATA_SAMPLE`.

Ampliación de deportes y juegos: pruebas acotadas de notación o registros reales; las tres preguntas son propuestas de investigación, sin hallazgos calculados.

**Prueba 1: `DATA_SAMPLE`** · [gcg](https://www.cross-tables.com/annotated/selfgcg/566/anno56686.gcg) · HTTP `200`.

Captura UTC: `2026-11-07T06:03:55+00:00`; duración: 3.093 s.

Dos primeros turnos puntuados del GCG; no se verificaron tablero, diccionario, ganador ni legalidad de las palabras.

Contenido: ``; 4,646 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| player | Samuel Kaplan | Joey Krafchick |
| action | CDFIIOO 8E FOCI | ?DEILNY H8 .NEDIbLY |
| points | 18 | 86 |
| total | 18 | 86 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "player": "Samuel Kaplan",
    "action": "CDFIIOO 8E FOCI",
    "points": 18,
    "total": 18
  },
  {
    "player": "Joey Krafchick",
    "action": "?DEILNY H8 .NEDIbLY",
    "points": 86,
    "total": 86
  }
]
```

</details>

### nba-elo

**Básquetbol: historia NBA/ABA y pronósticos Elo** — `DATA_SAMPLE`.

Ampliación de deportes y juegos: pruebas acotadas de notación o registros reales; las tres preguntas son propuestas de investigación, sin hallazgos calculados.

**Prueba 1: `DATA_SAMPLE`** · [csv](https://raw.githubusercontent.com/fivethirtyeight/data/master/nba-elo/nbaallelo.csv) · HTTP `200`.

Captura UTC: `2026-11-07T06:03:55+00:00`; duración: 3.42 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

Contenido: `text/plain; charset=utf-8`; 65,536 bytes leídos; alcance del hash: `response_prefix`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| game_id | 194611010TRH | 194611010TRH |
| date_game | 11/1/1946 | 11/1/1946 |
| team_id | TRH | NYK |
| opp_id | NYK | TRH |
| pts | 66 | 68 |
| opp_pts | 68 | 66 |
| elo_i | 1300 | 1300 |
| forecast | 0.64006501 | 0.35993499 |
| _iscopy | 0 | 1 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "game_id": "194611010TRH",
    "date_game": "11/1/1946",
    "team_id": "TRH",
    "opp_id": "NYK",
    "pts": "66",
    "opp_pts": "68",
    "elo_i": "1300",
    "forecast": "0.64006501",
    "_iscopy": "0"
  },
  {
    "game_id": "194611010TRH",
    "date_game": "11/1/1946",
    "team_id": "NYK",
    "opp_id": "TRH",
    "pts": "68",
    "opp_pts": "66",
    "elo_i": "1300",
    "forecast": "0.35993499",
    "_iscopy": "1"
  }
]
```

</details>

### jolpica-f1

**Fórmula 1: carreras, clasificación y resultados vía Jolpica** — `DATA_SAMPLE`.

Ampliación de deportes y juegos: pruebas acotadas de notación o registros reales; las tres preguntas son propuestas de investigación, sin hallazgos calculados.

**Prueba 1: `DATA_SAMPLE`** · [json](https://api.jolpi.ca/ergast/f1/2024/1/results.json?limit=2) · HTTP `200`.

Captura UTC: `2026-11-07T06:03:58+00:00`; duración: 2.995 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

Contenido: `application/json`; 1,842 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| season | 2024 |
| round | 1 |
| raceName | Bahrain Grand Prix |
| date | 2024-03-02 |
| Circuit.circuitName | Bahrain International Circuit |
| Results | [{&quot;number&quot;: &quot;1&quot;, &quot;position&quot;: &quot;1&quot;, &quot;positionText&quot;: &quot;1&quot;, &quot;points&quot;: &quot;26&quot;, &quot;Driver&quot;: {&quot;driverId&quot;: &quot;max_verstappen&quot;, &quot;permanentNumber&quot;: &quot;3&quot;, &quot;code&quot;: &quot;VER&quot;, &quot;url&quot;: &quot;http://en.wikipedia.org/wiki/Max_Verstappen&quot;, &quot;givenName&quot;: &quot;Max&quot;, &quot;familyName&quot;: &quot;Verstappen&quot;, &quot;dateOfBirth&quot;: &quot;1997-09-30&quot;, &quot;nationality&quot;: &quot;Dutch&quot;}, &quot;Constructor&quot;: {&quot;constructorId&quot;: &quot;red_bull&quot;, &quot;url&quot;: &quot;https://en.wikipedia.org/wiki/Red_Bull_Racing&quot;, &quot;name&quot;: &quot;Red Bull&quot;, &quot;nationality&quot;: &quot;Austrian&quot;}, &quot;grid&quot;: &quot;1&quot;, &quot;laps&quot;: &quot;57&quot;, &quot;status&quot;: &quot;Finished&quot;, &quot;Time&quot;: {&quot;millis&quot;: &quot;5504742&quot;, &quot;time&quot;: &quot;1:31:44.742&quot;}, &quot;FastestLap&quot;: {&quot;rank&quot;: &quot;1&quot;, &quot;lap&quot;: &quot;39&quot;, &quot;Time&quot;: {&quot;time&quot;: &quot;1:32.608&quot;}, &quot;AverageSpeed&quot;: {&quot;units&quot;: &quot;kph&quot;, &quot;speed&quot;: &quot;210.383&quot;}}}, {&quot;number&quot;: &quot;11… [ver JSON completo debajo] |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "season": "2024",
    "round": "1",
    "raceName": "Bahrain Grand Prix",
    "date": "2024-03-02",
    "Circuit.circuitName": "Bahrain International Circuit",
    "Results": [
      {
        "number": "1",
        "position": "1",
        "positionText": "1",
        "points": "26",
        "Driver": {
          "driverId": "max_verstappen",
          "permanentNumber": "3",
          "code": "VER",
          "url": "http://en.wikipedia.org/wiki/Max_Verstappen",
          "givenName": "Max",
          "familyName": "Verstappen",
          "dateOfBirth": "1997-09-30",
          "nationality": "Dutch"
        },
        "Constructor": {
          "constructorId": "red_bull",
          "url": "https://en.wikipedia.org/wiki/Red_Bull_Racing",
          "name": "Red Bull",
          "nationality": "Austrian"
        },
        "grid": "1",
        "laps": "57",
        "status": "Finished",
        "Time": {
          "millis": "5504742",
          "time": "1:31:44.742"
        },
        "FastestLap": {
          "rank": "1",
          "lap": "39",
          "Time": {
            "time": "1:32.608"
          },
          "AverageSpeed": {
            "units": "kph",
            "speed": "210.383"
          }
        }
      },
      {
        "number": "11",
        "position": "2",
        "positionText": "2",
        "points": "18",
        "Driver": {
          "driverId": "perez",
          "permanentNumber": "11",
          "code": "PER",
          "url": "http://en.wikipedia.org/wiki/Sergio_P%C3%A9rez",
          "givenName": "Sergio",
          "familyName": "Pérez",
          "dateOfBirth": "1990-01-26",
          "nationality": "Mexican"
        },
        "Constructor": {
          "constructorId": "red_bull",
          "url": "https://en.wikipedia.org/wiki/Red_Bull_Racing",
          "name": "Red Bull",
          "nationality": "Austrian"
        },
        "grid": "5",
        "laps": "57",
        "status": "Finished",
        "Time": {
          "millis": "5527199",
          "time": "+22.457"
        },
        "FastestLap": {
          "rank": "4",
          "lap": "40",
          "Time": {
            "time": "1:34.364"
          },
          "AverageSpeed": {
            "units": "kph",
            "speed": "206.468"
          }
        }
      }
    ]
  }
]
```

</details>

### opendota-partidas

**Videojuegos: partidas competitivas de Dota 2 en OpenDota** — `DATA_SAMPLE`.

Ampliación de deportes y juegos: pruebas acotadas de notación o registros reales; las tres preguntas son propuestas de investigación, sin hallazgos calculados.

**Prueba 1: `DATA_SAMPLE`** · [json](https://api.opendota.com/api/proMatches) · HTTP `200`.

Captura UTC: `2026-11-07T06:03:58+00:00`; duración: 2.995 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

Contenido: `application/json; charset=utf-8`; 31,144 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| match_id | 9078923915 | 9078644458 |
| start_time | 1793988383 | 1793977350 |
| duration | 2924 | 2195 |
| radiant_name | ветмо | null |
| dire_name | Party 2 play | null |
| radiant_win | false | true |
| radiant_score | 37 | 67 |
| dire_score | 61 | 24 |
| league_name | Party To Play league | 护鼠宝 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "match_id": 9078923915,
    "start_time": 1793988383,
    "duration": 2924,
    "radiant_name": "ветмо",
    "dire_name": "Party 2 play",
    "radiant_win": false,
    "radiant_score": 37,
    "dire_score": 61,
    "league_name": "Party To Play league"
  },
  {
    "match_id": 9078644458,
    "start_time": 1793977350,
    "duration": 2195,
    "radiant_win": true,
    "radiant_score": 67,
    "dire_score": 24,
    "league_name": "护鼠宝"
  }
]
```

</details>

## Evidencia y alcance

[Resultados JSON](results.json) · [Definiciones de tests](../../catalogs/source_probes.json) · [Manifest de pruebas visuales](../../catalogs/visual_examples.json) · [Catálogo](../../docs/CATALOGO_DATASETS_REALES.md)

El informe acumulado conserva las fechas y versiones del verificador en `results.json`: corrida inicial, ampliaciones y reintentos. Cada prueba visual guarda URL, HTTP, formato, dimensiones, bytes y hash de la respuesta completa. Decodificar una imagen no valida etiquetas, autenticidad histórica, OCR, contenido clínico ni representatividad de los datos.

## Validación del cambio

- **Fuentes:** 6/6 con `DATA_SAMPLE`; 8/8 peticiones con HTTP 200 y ejemplos reales. Se incluye PGN del mundial de 2021 y del archivo Carlsen, eventos de fútbol, turnos GCG y resultados deportivos.
- **Pruebas locales:** `python -m pytest -q tests` → **24 passed** (incluye 11 pruebas nuevas de lectura PGN/GCG, rechazo de HTML y lectura acotada de ZIP). Las pruebas unitarias usan fixtures sintéticos; los ejemplos de este README proceden de las respuestas públicas registradas.
- **Catálogo y rutas de análisis:** 78 fuentes, 234 preguntas, 17 temáticas; validación estructural aprobada con `python scripts/render_exploration_plan.py --check`. Las 72 evidencias anteriores se conservaron sin cambios.
- **Alcance:** se probó acceso y lectura de muestras; las 18 preguntas nuevas siguen abiertas. No se verificó la legalidad de todas las jugadas ni se ejecutaron motores o simuladores.
