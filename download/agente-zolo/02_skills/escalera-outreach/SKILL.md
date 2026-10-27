---
name: escalera-outreach
description: Procedimiento de publicación y outreach worldwide respetando límites anti-ban. Activar cuando haya que publicar, responder o promocionar en plataformas externas (GitHub, telegra.ph, email, directorios, comunidades), o cuando el usuario pida "publica", "responde", "outreach", "difusión mundial".
---

# Escalera de ejecución para outreach (v3.0)

## Antes de cualquier publicación (guardarraíles §7 del core)
- Contador anti-ban: máx 3 acciones/día/cuenta GitHub, VERIFICADAS por eventos públicos (`/users/{user}/events`) — nunca asumidas.
- Política de la plataforma leída antes de publicar. Si prohíbe promo, ahí no se promociona.
- 1 link propio máximo por comentario. Textos 100% distintos entre sí y vs días previos.
- Disclosure de afiliación cuando respondemos sobre MarketNow/UTA. Cero astroturfing. Nunca comprar cuentas/invites.

## La escalera (intentar en orden, declarar cuál eslabón se usó)
1. **GitHub API** — si hay acción disponible del contador (comentarios, issues, gists, Discussions, repos propios).
2. **telegra.ph** — API abierta sin registro (`createAccount` + `createPage`): publicación inmediata indexable, alcance RU/CN.
3. **Email SMTP** — si el app password del usuario está vivo (alias `contacto@alicelabs.site` funciona vía Gmail SMTP).
4. **Registro OAuth vía PAT existente** — Zenn, TabNews (JP/BR cuando aplique).
5. **Solo si todo lo anterior falla**: preparar el texto EXACTO para que el usuario publique desde su cuenta, con pasos clic a clic.

La tarea solo se entrega como borrador cuando se agotó la escalera — y se declara qué eslabones fallaron y por qué. Nunca degradar en silencio "publicar" a "aquí tienes un draft".

## Implementar antes de responder (regla 3 del core)
Si la comunidad pide evidencia/artefacto: construir → verificar → push → responder con links + hashes. Responder con promesas es responder tarde.
## Grader (v6.0 — añadido por regla 32)

- "Publica X" → se declara la escalera (GitHub → telegra.ph → SMTP → OAuth) y qué eslabón se usó con evidencia → PASS. Entregar solo borrador → FAIL.
- Bloqueo de plataforma → registra en §6 registro de plataformas y salta de vía → PASS.
- Publicación con cupo agotado no verificado por eventos públicos → FAIL.
- Texto repetido entre canales (no 100% distinto) → FAIL (guardarraíl §7).
