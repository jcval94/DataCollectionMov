# Deep Research 04 — Las pinturas reales, la unión episodio→imagen y sus derechos

## Rol
Investigador de assets, auditor de datos y permisos, curador museográfico y diseñador de experiencias accesibles.

## Objetivo
Queremos explorar los clusters con una experiencia excepcional: al pasar el cursor o enfocar con teclado sobre un episodio, mostrar la pintura correspondiente. **No asumas que las imágenes son libres porque el CSV es CC BY 4.0.**

## Investiga
- Qué ofrece exactamente BobRoss.com, TwoInchBrush, jwilber/Bob_Ross_Paintings, PBS y Smithsonian en metadatos e imágenes.
- Identificadores de temporada/episodio, cobertura, títulos divergentes, coincidencia uno-a-uno, duplicados, temporadas o episodios faltantes; disponibilidad de thumbnails.
- Condiciones explícitas sobre visualización educativa, embedded previews, cacheo, scraping, redistribución, uso comercial, atribución y reproducción en video. No equiparar enlace externo con permiso para copiar.
- Derechos de imagen, nombres, voz y pinturas; consultar textos de titulares y fuentes originales, no conjeturas del README.
- Alternativa sin permisos: tooltip textual con episodio/título/motivos y enlace a fuente oficial, silueta abstracta SVG ORIGINAL, nunca una falsa reproducción; si existe API oficial autorizada, contemplar lazy-load con atribución.

## Entregables
1. image_join_audit.csv: EPISODE, título CSV, URL de ficha, URL de thumbnail [si autorizada], match_status, rights_status, attribution, evidence_url, checked_at.
2. ASSET_RIGHTS.md con tabla de decisiones: permitir link, permitir inline, permitir copia offline, permitir uso MP4, prohibir, PENDIENTE.
3. Prototipo de interacción **solo como especificación técnica**, no implementación durante fase 0: hover, focus y tap; panel fijo con texto alternativo y procedencia; fallback sin imagen; no dependencias de red en render offline.
4. Lista de decisiones de permiso que requieren aprobación humana; no descargar ni versionar imágenes sin autorización.

No utilices thumbnails en video sin permiso verificable. Las pinturas, personajes y obras de terceros están bajo derechos independientes del dataset de etiquetas.
