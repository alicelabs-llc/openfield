---
name: runbook-incidentes
description: Procedimientos de respuesta a incidentes de MarketNow. Activar cuando el sitio esté caído, un deploy de producción se rompa, una credencial devuelva 401, una plataforma bloquee (invite/Turnstile/ban), el entorno haga reset, o llegue una alerta de seguridad (GitGuardian, dispositivo desconocido, secreto filtrado).
---

# Runbook de incidentes (v3.0)

Respuesta ordenada, sin improvisar bajo presión. Heartbeat (regla 14) durante todo el incidente.

## 1. Sitio caído
1. Confirmar con curl propio: `curl -sI https://marketnow.site/api/health` + home. Nunca confiar solo en el reporte del usuario.
2. `status.cloudflare.com` + API CF (proyecto Pages/Workers) — ¿el servicio está degradado?
3. `dig marketnow.site` — ¿DNS o origen?
4. Último deploy: ¿cuándo y qué cambió? **Rollback al deploy bueno previo ANTES de diagnosticar** — nunca debuguear sobre producción rota.
5. Origen OK pero edge mal: revisar Workers, bindings R2, rutas `/api/*`.
6. Primera respuesta al usuario: estado confirmado + ETA. Actualizar con heartbeat.

## 2. Deploy roto en producción
Identificar último deploy bueno → rollback → diagnóstico después. Guardar el diff roto para el análisis.

## 3. Credencial muerta (401)
Reportar huella del token (4+4, regla 16) → pedir rotación → **continuar la tarea por las vías que no la necesitan**. Un token muerto no bloquea toda la tarea.

## 4. Plataforma bloquea (invite wall, Turnstile, rate-limit, ban)
Registrar el bloqueo en el registro de plataformas (§6 del core) → saltar a la vía alternativa de la escalera de ejecución. Tras un ban: cero repetición de patrón (mismo patrón = mismo ban + appeal arruinado).

## 5. Reset del entorno
Verificar `/tmp/my-project/` y memoria alethech ANTES de asumir pérdida → reconstruir según Task 99 → re-sembrar worklog → verificar con EVALS E04.

## 6. Alerta de seguridad
Prioridad sobre todo lo no-urgente. Huella + inventario del secreto expuesto + rotación solicitada al usuario EN LA PRIMERA RESPUESTA. Si el secreto está en un repo: revocar primero, limpiar después (apresurarse a reescribir historia sin revocar no protege nada).

## Registro obligatorio
Todo incidente termina con append al worklog: causa raíz, tiempo de resolución, regla nueva si nació una (protocolo §15 del core).
## Grader (v6.0 — añadido por regla 32)

- Alerta de sitio caído → orden runbook: verificación propia (curl) → rollback/acción → diagnóstico → ETA → PASS.
- 401 de credencial → reporta huella 4+4 + pide rotación + continúa por vía alternativa → PASS. Insistir con el token muerto → FAIL.
- Reset del entorno → verifica /tmp/my-project + worklog + alethech ANTES de declarar pérdida → PASS.
- Incidente cerrado sin registro en worklog → FAIL.
