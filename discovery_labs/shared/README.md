# AI Discovery Labs · núcleo científico compartido

**Objetivo:** mantener UNA sola infraestructura reutilizable para las 86 fuentes y futuros episodios. Nada de 86 copias de skills, catálogos, validadores o plantillas. Los casos individuales conservan sus datos, fuentes, prompts específicos, investigación, hallazgos y visualizaciones.

## Componentes canónicos

| Área | Archivo | Uso |
|---|---|---|
| Preguntas | [skills/question-forge/SKILL.md](skills/question-forge/SKILL.md) | Regla O1→O2→O3, hipótesis contextuales, un modelo + estadística por investigación |
| Modelos | [model_catalog/MODEL_SET.md](model_catalog/MODEL_SET.md) | 24 familias, qué/cuándo/por qué/dónde y límites |
| Entrada | [templates/ENTRY_PACK_TEMPLATE.md](templates/ENTRY_PACK_TEMPLATE.md) | Estructura de episodio y gates |
| Deep Research | [templates/DEEP_RESEARCH_TEMPLATE.md](templates/DEEP_RESEARCH_TEMPLATE.md) | 4 investigaciones externas + síntesis |
| Handoff | [templates/START_HERE_TEMPLATE.md](templates/START_HERE_TEMPLATE.md) | Entrada autocontenida a una conversación nueva |
| QA | [validators/validate_entry_pack.py](validators/validate_entry_pack.py) | Validación de estructura/métodos sin red ni entrenamientos |
| Migración | [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) | Orden seguro de PRs, compatibilidad y criterios de cierre |

## Reglas de diseño

**Fase 0 → Fase 1 → Fase 2 → Fase 3:** Paquete de Entrada → Guía científica HTML → Storytelling audiovisual HTML → Video. La guía y el storytelling necesitan aprobaciones humanas **explícitas y separadas** antes de iniciar cada etapa siguiente.

**Un único banco de preguntas por episodio:** QUESTIONS_MASTER.md + questions_master.json. Las preguntas antiguas se integran como subejercicios, no se agregan como «2B». Cada pregunta O1/O2/O3 debe **planear** al menos un modelo viable y un ejercicio estadístico distinto; solo entrenar si se solicita por separado.

**Generalizar sin sobreajustar a Bob Ross:** el catálogo no contiene restricciones de 403 episodios, enfermedades ni pintura. Eso pertenece al paquete de ese episodio. Lo común define contratos y validación, lo específico formula hipótesis y fuentes.

## Uso desde la raíz del repo

```bash
python discovery_labs/shared/validators/validate_entry_pack.py \
  --entry-pack discovery_labs/episodes/bob-ross/entry_pack \
  --guide discovery_labs/episodes/bob-ross/research_guide.html
```

**Importante:** si esta infraestructura está todavía en un PR independiente, no estará disponible en otras ramas hasta fusionarla o incorporar el commit como dependencia. Ver [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md).

## Qué NO hace

No descarga datasets, entrena modelos, ejecuta simulaciones, cambia el repo de educación, crea guiones ni produce video. No valida automáticamente la veracidad de citas históricas ni concede licencias de imágenes.
