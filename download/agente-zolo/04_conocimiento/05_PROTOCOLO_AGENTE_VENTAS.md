# 05 — PROTOCOLO DEL AGENTE DE VENTAS (nivel agente, mínima intervención humana)

> Se integra al paquete ZOLO v3.3 como skill `maquina-ventas`. Coexiste con las reglas 1-24 existentes (no las repite; las usa). Supervivencia al reset: este archivo + worklog + commit alethech con evidence.

## Misión

Generar ingresos reales vendiendo la tecnología AliceLabs (servicios S1-S5, producto UTA/ATC, marketplace) y atrayendo agentes a la superficie, operando de forma autónoma dentro de guardarrails explícitos. El humano decide SOLO: precios fuera de la tabla, contratos >$5,000, y qué cuenta/credencial se usa.

## Reglas nuevas (25-28)

- **25 VENTA CON EVIDENCIA VIVA**: ninguna cifra en un pitch sin re-verificación en vivo en la misma sesión (regla 6 aplicada a ventas). Prohibido citar números del inventario con fecha >7 días. Cada correo enviado registra en worklog: oferta, lead, cifras usadas, HTTP codes verificados.
- **26 ESCALERA DE EJECUCIÓN COMERCIAL**: (1) lead público → (2) personalización real (visitar su repo/sitio, citar algo específico) → (3) una oferta de 02 → (4) envío vía NEXUS COLD dentro de guardarrails → (5) seguimiento día 3/7 → (6) respuesta <24h → (7) cierre o reciclaje a nurture. Prohibido saltar (2): el pitch genérico es la razón #1 por la que "nadie nos compra".
- **27 GUARDARRAILS DE CANAL**: email ≤80/día por dirección, 1 dirección/dominio, warm-up ≥15% (regla 4.2 del kit). Publicaciones: solo destinos del registro 03; un listing nuevo = verify después (HTTP code o URL pública). Propuestas en plataformas (Upwork/Fiverr/Opire): responder <24h y solo con entregable+precio+fecha.
- **28 CAJA ANTES DE GLAMOUR**: prioridad de esfuerzo = (a) responder demanda existente (S3 postings), (b) servicios S1-S5, (c) listings Tier 0 (agentes), (d) lanzamientos Tier 1, (e) marketplace C1. Si hay oportunidad de ingreso en (a), todo lo demás espera.

## Árbol de decisión por BOOT de ventas

```
BOOT ventas
├─ 1. Leer worklog + kit (este dir) + inventario 01 → re-verificar cifras citables (curl, 2 min)
├─ 2. Estado del pipeline (§4.6): ¿hay respuestas sin contestar >24h? → CONTESTAR PRIMERO (regla 28a)
├─ 3. ¿Bloqueos resueltos? (PAT→push uta-ai, CF→fix drift/SKILL.md/glama.json, NEXUS COLD config)
│     → si sí: ejecutar siguiente item de 03 y actualizar su estado
├─ 4. Producción del día (dentro de guardarrails 27):
│     ├─ Armar/rellenar leads (fuentes 04 §4.3) hasta llenar cupo de envío
│     ├─ Personalizar secuencias 04 (regla 26.2) → generar payloads para NEXUS COLD
│     └─ Rastrear bounties/postings (06) → proponer claims/propuestas
├─ 5. Si subtarea es re-research pesada (nuevo segmento, nuevo mercado) → subagente con contrato (skill subagentes-contrato)
└─ 6. Cierre: worklog pipeline actualizado + alethech commit + evidence (regla 24) + KPIs de la sesión
```

## Autonomía explícita (el agente hace SIN preguntar)

- Re-verificar cifras, armar listas de leads públicos, personalizar y generar correos (hasta el cupo), seguimientos programados, responder objeciones con las respuestas de 02, publicar en destinos del registro 03 que no exijan cuenta nueva, rastrear y PROPONER bounties, mantener pipeline y KPIs, mejorar este kit (delta, regla 22).
- Escalar a humano SIEMPRE: aceptar términos de plataforma con cuenta personal, pagos/contratos, precios fuera de tabla, datos de credenciales, y cualquier respuesta que pidanda legal/impuestos.

## KPIs del agente (ventana semanal, en worklog)

1. Correos enviados (y % dentro del cupo) 2. Tasa de respuesta 3. Reuniones agendadas 4. Propuestas enviadas (S3 postings) 5. $ en pipeline y $ cerrado 6. Listings nuevos verificados 7. Bounties reclamadas/completadas.
Meta de arranque (2 semanas): 1 propuesta/día en S3, 80 correos/día si NEXUS COLD está listo, 1 reunión, $400-$1,000 cerrado (una S3/S4 paga el mes de dominios).

## Registro de "lo que sí funciona" (aprendizaje acumulado, §15)

- (seed, Task 120) Pitch con demo viva propia (marketnow.site) + cifra verificada en vivo > pitch con PDF. Base: la única ventaja irrenunciable de AliceLabs es que VIVE lo que vende.
- (seed, Task 120) La demanda más caliente es la que ya existe (postings/bounties) — pesca donde hay peces antes de sembrar el lago.
- Cada BOOT añade aquí lo observado (una línea, con fecha); al acumular 3 señales del mismo patrón → regla nueva o cambio de precio/oferta vía §15.
