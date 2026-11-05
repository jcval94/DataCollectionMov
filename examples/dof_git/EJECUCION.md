# Ejecución real de la demostración Git

UTC: 2026-11-05T00:04:35+00:00

Repositorio temporal, eliminado al terminar. Los hashes pertenecen a esta ejecución local.

```text
$ git log --oneline --reverse
948bd6c Representar el mínimo anterior a la reforma de vacaciones
d280643 Representar el cambio publicado en DOF el 27-12-2022

$ git diff HEAD~1 HEAD -- articulo_76.json
diff --git a/articulo_76.json b/articulo_76.json
index 3ab7976..49b7b55 100644
--- a/articulo_76.json
+++ b/articulo_76.json
@@ -2,5 +2,5 @@
   "representacion": "Resumen didáctico de un parámetro; no es texto legal consolidado",
   "norma": "Ley Federal del Trabajo",
   "articulo": 76,
-  "minimo_anual_dias_laborables": 6
+  "minimo_anual_dias_laborables": 12
 }

$ git blame -L 5,5 -- articulo_76.json
d2806432 (Demo didáctica 2026-11-04 18:04:35 -0600 5)   "minimo_anual_dias_laborables": 12

Comprobación: 2 commits, un único dato modificado y árbol de trabajo limpio.
```
