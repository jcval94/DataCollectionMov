# DOF para explicar Git: ¿quién cambió el dato y cuándo?

Caso real: el decreto publicado el **27 de diciembre de 2022** reformó los artículos 76 y 78 de la Ley Federal del Trabajo. Para mostrar Git, reducimos el cambio del mínimo anual del artículo 76 a **un dato: 6 → 12 días laborables**. Los JSON son resúmenes didácticos de ese parámetro; no reproducen ni sustituyen el texto normativo completo.

## Fuentes del ejemplo

| Evidencia | Fuente y alcance |
| --- | --- |
| Parámetro anterior: 6 | [Expediente legislativo y cuadro comparativo, Cámara de Diputados](https://www.diputados.gob.mx/sedia/biblio/prog_leg/Prog_leg_LXV/103_DOF_27dic22.pdf), columna de texto vigente anterior. Fuente primaria localizada en búsqueda; su descarga excedió el límite adicional de 12 MB y no se verificó todo el PDF. También consta en esta [publicación histórica de PROFEDET](https://www.gob.mx/profedet/es/articulos/trabajador-y-trabajadora-al-cumplir-un-ano-de-servicios-tu-patron-te-debe-otorgar-vacaciones), cuyo contenido histórico está indexado, aunque el acceso directo devolvió 403. |
| Parámetro reformado: 12 | [Nota oficial SIDOF 5675889](https://sidof.segob.gob.mx/notas/docFuente/5675889). Texto recuperado y comprobado por la prueba `dof-publicaciones`. |
| Fecha de publicación y transitorio | [Ficha de la nota](https://sidof.segob.gob.mx/notas/5675889): publicación 2022-12-27. El decreto señala entrada en vigor 2023-01-01 para este caso. Son fechas distintas. |

## La analogía, con sus límites

| En Git | En este ejemplo |
| --- | --- |
| Repositorio | Carpeta con la representación y sus fuentes. |
| Commit | Captura intencional de un estado del archivo y mensaje que explica su cambio. |
| `git log` | Historial de las dos capturas, con identificador de cada una. |
| `git diff` | Cambio exacto de `6` a `12` en el mismo campo. |
| `git blame` | Identifica el commit local que introdujo el valor actual. No identifica al legislador ni prueba autoridad jurídica. |
| Rama | Permite ensayar una interpretación o extracción alternativa sin sustituir la versión principal. Es una analogía pedagógica, no una función del DOF. |
| Merge | Integra cambios del trabajo de extracción/revisión; no convierte propuestas en normas. |

El DOF publica documentos nuevos. Una reforma no borra la publicación anterior. La representación consolidada es un trabajo adicional y Git sólo registra lo que nosotros guardamos: ni valida legalidad ni resuelve por sí mismo la vigencia de una ley. Para cotejar el contenido publicado, la propia ficha SIDOF remite a la edición digitalizada/PDF si la conversión HTML pierde elementos.

## Práctica de dos minutos

Desde la raíz del repositorio, con Python y Git instalados:

```bash
python examples/dof_git/demo_git.py
```

El programa crea un repositorio temporal sin remotos, guarda `antes.json` en el primer commit y `despues.json` en el segundo. Muestra `log`, `diff` y `blame`, comprueba los dos commits y elimina únicamente su carpeta temporal al terminar. No cambia la configuración global de Git ni el repositorio del usuario.

La demostración usa la fecha real de ejecución para sus commits. La fecha histórica de la reforma se conserva en el mensaje y las fuentes; no se falsifican fechas de commits ni se presenta este historial como un repositorio oficial.

Para guardar tu ejecución:

```bash
python examples/dof_git/demo_git.py --report /tmp/ejecucion_dof_git.md
```

Revisa la [ejecución comprobada](EJECUCION.md) y las [pruebas de las fuentes del catálogo](../../source_tests/README.md).

Pregunta para clase: si alguien cambia `12` por `120`, ¿qué comando muestra la diferencia, cuál identifica el commit y por qué ese historial no basta para validar el contenido?
