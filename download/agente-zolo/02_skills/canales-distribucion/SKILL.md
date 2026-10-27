---
name: canales-distribucion
description: Canales de distribución para lanzamientos (v6.0 — reel 8 del founder). Activar cuando se lanza una app/repo/producto y toca publicarlo, cuando el founder pide "dónde lo publicamos" o "que la gente lo pruebe", o al planificar una semana de lanzamiento. Cubre los 5 canales de arranque con sus reglas específicas, el orden correcto y su integración con los guardarraíles anti-ban.
---

# Canales de distribución — los 5 primeros lugares, no "todas partes" (v6.0)

Fuente (reel 8 del founder, Task 123): "¿Lanzaste tu app y nadie la usa? No la publiques en todas partes. Empieza por estos 5 sitios." Integración con: `escalera-outreach` (ejecución multi-canal real), §6 registro de plataformas (qué puedo ejecutar yo vs cuenta del usuario), §7 guardarraíles anti-ban (SIEMPRE primero).

## 1. Los 5 canales de arranque (en este orden de prueba)

| # | Canal | Qué lo hace bueno | Regla de ejecución |
|---|---|---|---|
| 1 | **Reddit — r/SideProject** | Creadores prueban apps nuevas y te dicen QUÉ está mal — feedback crudo antes de escalar | Post honesto ("lo construí, busco feedback"), responder TODO comentario en <24h, cero lenguaje de anuncio. Subreddits adicionales según producto (reglas de cada sub ANTES de postear — §7) |
| 2 | **Hacker News** | Portada = miles de visitas en un día | Show HN con título técnico exacto, primera doc/README impecable, responder comentarios sin marketing (la comunidad huele el pitch). Fallar el lanzamiento es normal — no insistir el mismo día |
| 3 | **Product Hunt** | Audiencia de early-adopters con volumen | Lanzar **martes/miércoles/jueves** (más tráfico de votantes); kit visual listo (logo, galería, tagline de 1 línea); el founder/usuario hace la parte de cuenta (§6: login del usuario) |
| 4 | **Indie Hackers** | Founders que sí prueban cosas nuevas y compran herramientas | Post con métricas reales y la historia de construcción (esa comunidad premia transparencia) |
| 5 | **Uneed** | Plataforma menor donde el producto NO se pierde el día 1 + link directo al sitio | Aprobar primero los 4 anteriores; Uneed da cola larga sin competencia brutal |

## 2. El orden ES la estrategia

1. **r/SideProject primero** → feedback destructivo barato (mejor un comentario duro ahí que 20 en HN).
2. Arreglar lo señalado (skill `depuracion-sistematica` si hay bugs; ledger de feedback en `06_aprendizaje/LEARNINGS.md` — cada queja es insight).
3. **HN después** con el producto ya endurecido.
4. **Product Hunt** en ventana Tue-Thu con lo aprendido.
5. **Indie Hackers + Uneed** como cola de largo aliento.
Publicar en TODOS lados el mismo día = quemar el lanzamiento (cada canal pide su propia madurez).

## 3. Insight de canal adicional (reel 3): plugins como distribución

El store de plugins de ChatGPT es hoy lo que la App Store fue en 2008 (caso citado: $500K ARR proyectados en la 1ª semana de un plugin). Para productos de AliceLabs: cada superficie nueva (plugin, skill instalable, MCP server) es un CANAL — ver skill `iniciativa-agent-first` (regla 23). El distribution-first thinking: "plugins para negocios que no saben que los necesitan" = oferta S1-S2 del kit de ventas vista como canal, no como producto.

## 4. Ejecución YO vs TÚ (regla 2 del núcleo)

- **YO**: texto exacto por canal (100% distinto entre canales), timing recomendado, kit visual copiable, respuesta a comentarios en plataformas donde tengo vía (GitHub, dev.to, telegra.ph), medición post-lanzamiento (curl de analytics, inventario de menciones).
- **TÚ (cuenta del usuario)**: logins de Reddit/HN/Product Hunt (§6) — yo preparo clic-a-clic lo que toca pegar.
- Guardarraíles §7 SIEMPRE: 3 acciones/día/cuenta, políticas primero, 1 link propio, disclosure de afiliación, cero astroturfing (NUNCA cuentas falsas "probando" el producto).

## 5. Grader

- Cualquier plan de lanzamiento nombra los 5 canales EN ORDEN con la madurez que exige cada uno → PASS.
- "Publica en todas partes hoy" ejecutado literal sin orden → FAIL (la estrategia es la secuencia).
- Post de Reddit con lenguaje de anuncio en vez de feedback-seeking → FAIL.
- Product Hunt fuera de Tue-Thu sin justificación → WARN.
- Feedback recibido (aunque sea duro) registrado en el ledger → PASS.

## Grader (regla 28)

```bash
test_canales-distribucion() {
    # 1. Skill existe con frontmatter
    test -f 02_skills/canales-distribucion/SKILL.md
    # 2. Frontmatter tiene name y description
    grep -q "^name:" 02_skills/canales-distribucion/SKILL.md
    grep -q "^description:" 02_skills/canales-distribucion/SKILL.md
    # 3. Skill indexada en §12 del núcleo
    grep -q "canales-distribucion" 01_nucleo/ZOLO_V6.md
}
```
