---
name: diseno-web-premium
description: Diseño web premium anti-slop (v6.0 — reel 1 del founder). Activar al construir o revisar CUALQUIER interfaz (landing, dashboard, app, página del sitio, demo para cliente). Cubre: inferencia de brief, sistema de diseño completo, reglas de prioridad UX 1-10, par build+audit con subagentes, auditoría anti-slop en navegador real a 3 anchos y checklist de entrega. Usar también cuando el founder pida "que no se vea hecha con IA".
---

# Diseño web premium — contra el AI-slop (v6.0)

Fuentes verificadas (reel 1 del founder, Task 123): `Leonxlnx/taste-skill` (anti-slop frontend, estudio de 247 sitios) · `nextlevelbuilder/ui-ux-pro-max-skill` (~100k★, 79 estilos, 192 paletas, 74 pares tipográficos, 119 guías UX) · `impeccable` (slop-checker) · patrón "subagentes que construyen y auditan". Repos clonados en `repos/Leonxlnx_taste-skill/` y `repos/nextlevelbuilder_ui-ux-pro-max-skill/`. Complementa: `flota-produccion` (par constructor/auditor) y `frontend-design` de `anthropics/skills` (en `repos/anthropics_skills/`).

## 1. Por qué existe este skill

"Tu página hecha con IA se ve igual que la de todos. No es la IA: te faltan las herramientas." El slop no es falta de modelo, es falta de MÉTODO: el modelo por defecto tiende a las mismas elecciones (gradientes púrpura-rosa, Inter, cards genéricas, emoji como iconos, secciones de desiguales anchos). Este skill sustituye el gusto ausente por un PROCESO verificable.

## 2. Fase A — Inferencia del brief (antes de abrir el editor)

Responder en 5 líneas: industria · audiencia · emoción objetivo (qué debe SENTIR) · profundidad de movimiento (sobrio/vivo) · familia de layout (hero-centric, editorial, bento, dashboard, app-shell). Declarar lo que SOLO tiene este cliente (su material propio: datos, fotos, casos, marca) — la diferenciación nace de ahí, no del CSS.

## 3. Fase B — Sistema de diseño (no "estilos sueltos")

Producir el bloque de sistema ANTES de maquetar:
- **Patrón de página** y orden de secciones (ej. Hero → prueba social → servicios → CTA repetido tras testimonios → contacto).
- **Paleta**: primario, secundario, CTA, fondo, texto + RAZÓN por tipo de producto (spa ≠ fintech ≠ dev-tool). Prohibido el combo púrpura/rosa por defecto de IA salvo mandato de marca.
- **Tipografía**: 1 par con intención (serif editorial + sans neutra, etc.), base 16px, line-height 1.5, jerarquía de 3 niveles máximo.
- **Efectos clave**: sombras suaves, transiciones 150-300ms, hover con estado — un solo lenguaje de movimiento en toda la página.
- **Anti-patrones prohibidos** (de ui-ux-pro-max + taste): gradientes AI por defecto · emoji como iconos (usar SVG) · mezclar esqueumorfismo con flat · texto <12px · gris sobre gris · animaciones duras · dark mode sin decisión de marca · secciones empujadas a un lado · tramos en blanco aleatorios.

## 4. Fase C — Reglas de prioridad UX 1→10 (revisar en este orden)

| # | Categoría | Impacto | Chequeos mínimos |
|---|---|---|---|
| 1 | Accesibilidad | CRÍTICO | Contraste 4.5:1, alt text, navegación por teclado, aria-labels |
| 2 | Touch e interacción | CRÍTICO | Mínimo 44×44px, separación 8px+, feedback de carga |
| 3 | Performance | ALTO | WebP/AVIF, lazy loading, espacio reservado (CLS < 0.1) |
| 4 | Selección de estilo | ALTO | Coherencia con producto, iconos SVG |
| 5 | Layout responsive | ALTO | Mobile-first, sin scroll horizontal, viewport meta |
| 6-10 | Tipografía/color, contenido, confianza, conversión, detalle | MEDIO | Tokens semánticos, copy real (no lorem), prueba social, CTA visible |

## 5. Fase D — Producción con flota (par build + audit)

1. Subagente **constructor** con el sistema de diseño como spec (Fase B) y reglas 1-5 como restricciones.
2. Subagente **auditor escéptico** (flota-produccion §6): revisa en navegador real (Playwright/MCP) a **3 anchos** (móvil ~390px, tablet ~768px, desktop ~1440px), captura screenshots y FALLA la entrega si encuentra slop (grep del anti-patrón + inspección visual de screenshots — el screenshot es la verdad de superficie, el DOM da los números).
3. Fix loop: top 3 problemas por ronda, máx 3 rondas (patrón taste-skill: ~30-45 min de build, el rigor ES el producto).

## 6. Fase E — Checklist de entrega (pre-flight)

- [ ] Título claro en la primera pantalla + márgenes iguales + ninguna sección descentrada
- [ ] Sin emoji como iconos; iconografía de una sola familia
- [ ] Contraste 4.5:1 verificado (o documentado el caso excepcional)
- [ ] Imágenes reales de colecciones abiertas (Wikimedia/Openverse/Met, CC0-CC BY) CON créditos — nunca placeholders rotos
- [ ] Animaciones con `prefers-reduced-motion` respetado
- [ ] Screenshots de 3 anchos adjuntos como evidencia + lista de problemas fixeados por ronda
- [ ] La página ¿se distingue de "hecha con IA por defecto"? (si un auditor la confunde, volver a Fase A)

## 7. Grader

- Fase A-B declaradas ANTES de maquetar → PASS.
- Auditoría en navegador real a 3 anchos con screenshots → PASS (solo DOM sin screenshots = FAIL).
- Emoji como iconos o gradiente AI por defecto sin justificación de marca → FAIL.
- Cada ronda de fix con top-3 problemas y evidencia → PASS.

## 8. Fuentes en disco

`repos/Leonxlnx_taste-skill/` (proceso de 6 pasos + bans + motion) · `repos/nextlevelbuilder_ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL.md` (tabla de prioridad + datos buscables) · `repos/anthropics_skills/skills/frontend-design/` (referencia oficial). Re-clonar: ver `02_skills/biblioteca-skills/FUENTES.md`.

## Grader (regla 28)

```bash
test_diseno-web-premium() {
    # 1. Skill existe con frontmatter
    test -f 02_skills/diseno-web-premium/SKILL.md
    # 2. Frontmatter tiene name y description
    grep -q "^name:" 02_skills/diseno-web-premium/SKILL.md
    grep -q "^description:" 02_skills/diseno-web-premium/SKILL.md
    # 3. Skill indexada en §12 del núcleo
    grep -q "diseno-web-premium" 01_nucleo/ZOLO_V6.md
}
```
