# Migración segura de Bob Ross a infraestructura compartida

## Grafo de dependencia de PRs

- **PR original #5** (episodio base): rama `feat/bob-ross-discovery-episode-only` → `main`. Es un borrador y puede tener trabajo de otro agente; no reescribir ni fusionar por esta extracción.
- **PR de Question Forge #10** (Paquete de Entrada): rama `feat/bob-ross-entry-pack-question-forge`, base `feat/bob-ross-discovery-episode-only`. Es un PR apilado y no se debe retargetear sin inspeccionar el diff y la aprobación.
- **Este PR independiente del motor compartido**: rama `feat/discovery-labs-shared-research-core` → `main`. Contiene exclusivamente `discovery_labs/shared/`.

## Orden recomendado

1. Revisar y aprobar el PR compartido **primero**, con la skill, modelo, plantillas y QA genéricos.
2. Integrarlo en `main` cuando esté listo; no asumir CI verde sin ejecución.
3. Actualizar PR #5 y #10 frente a la rama principal, respetando trabajo concurrente.
4. **Migrar PR #10** (no este PR) a una única fuente: referencias del Paquete de Entrada apuntan a `discovery_labs/shared/`. Sustituir sus copias de SKILL.md y MODEL_SET.md por stubs de compatibilidad o eliminarlas solo tras verificar enlaces, validadores y consumidores.
5. Los modelos que **sí son específicos de Bob Ross** (403 registros, 31 temporadas, invitado n=22, ausencia de variables clínicas, límites de imagen/paleta) deben ir en `entry_pack/MODEL_FIT_BOB_ROSS.md` y no en el catálogo central.
6. Ejecutar el validador compartido y los tests del episodio en la rama que contenga ambas capas.
7. Inspeccionar PR #10 (actualmente draft/mergeability variable), revisar conflictos reales, asegurar que el diff no sale de Bob Ross **excepto la infraestructura del PR compartido** ya integrada.

## Compatibilidad segura

**Hasta que el nuevo PR de shared esté fusionado o incluido explícitamente en la rama del episodio, las rutas previas dentro de Bob Ross deben seguir funcionando.** No eliminar las copias antiguas prematuramente. Si el consumidor corre `entry_pack/validate_pack.py`, no apuntarlo a shared hasta que shared realmente esté disponible en esa rama. Al migrar, reemplazar duplicados por referencias explícitas, conservar links e historial, documentar un orden de despliegue.

## Criterio de cierre

- [ ] Shared integrado en main.
- [ ] Skill V2.1 y catálogo 24 familias disponibles sin depender de Bob Ross.
- [ ] Validación genérica ejecutada en al menos dos episodios con inputs distintos (Bob Ross y otro piloto).
- [ ] Bob Ross referenciando shared, sin fuentes duplicadas mantenidas.
- [ ] Guía científica Bob Ross aún bloqueada para storytelling/video hasta aprobación.
- [ ] PR #5 y #10 revisados y sin conflictos pendientes antes de su fusión.

Esta extracción introduce **una dependencia de integración**, no declara que toda la migración esté terminada.
