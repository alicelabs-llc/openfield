---
name: cumplimiento-legal-vibecoding
description: Checklist legal para apps lanzadas con IA (v6.0 — reel 12 del founder: "con 0 ventas ya puedes deber $100,000"). Activar ANTES de publicar/entregar cualquier app, landing con formularios, o producto que recolecte datos — propia o de cliente. Cubre COPPA, fuentes self-hosted, grabación de sesiones, emails de marketing, términos de suscripción y DMCA, más el patrón de corrección por prompt.
---

# Cumplimiento legal de vibe coding — el checklist de los 6 puntos (v6.0)

Fuente (reel 12 del founder, Task 123): con cero ventas ya existe exposición legal — el coste de no cumplir es independiente del ingreso. Este skill convierte el reel en protocolo verificable de pre-lanzamiento. Alcance: revisión técnica de cumplimiento en el código/superficie; NO es asesoría legal formal (las decisiones jurídicas las toma el founder o un abogado — declararlo cuando aplique).

## 1. Los 6 puntos obligatorios ANTES de publicar

| # | Riesgo | Chequeo técnico en el producto |
|---|---|---|
| 1 | **COPPA (menores de 13)** | ¿Hay verificación de edad/fecha en el registro si el producto puede atraer menores? Sin ella en un producto para el público general = riesgo alto. Añadir gate de edad y política de menores |
| 2 | **Google Fonts (GDPR/privacidad)** | ¿Las fuentes se cargan desde fonts.googleapis.com? La IP del usuario viaja a Google (multas en la UE). Hostear las fuentes en el propio dominio (self-host woff2) o usar sistema |
| 3 | **Grabación de sesiones / telemetría** | ¿Hay replay/heatmaps/rastreo? Debe estar OFF por defecto, con opt-in claro, y enmascarar TODOS los campos de formulario (inputs, passwords, tarjetas) en cualquier captura |
| 4 | **Emails de marketing (CAN-SPAM/LSSI)** | Cada email comercial lleva link de unsubscribe funcional + dirección postal física del remitente. Sin ambos = infracción por cada email enviado |
| 5 | **Suscripciones y renovación** | Cerca del botón de pago: términos de renovación visibles (precio, frecuencia, cómo cancelar) SIN scroll ni acordeón escondido. Cancelación tan fácil como la contratación |
| 6 | **DMCA (contenido de terceros)** | Página/agente DMCA designado + proceso de takedown documentado. En EE.UU. el safe harbor del copyright exige el agente registrado (copyright.gov) — sin él, el contenido subido por usuarios puede costar la plataforma entera |

## 2. Capa 2 (recomendada si hay usuarios reales)

- Política de privacidad accesible en 1 click desde TODAS las páginas que recolecten datos (URL real, no "próximamente").
- Consentimiento de cookies razonable para la audiencia (UE = banner real con rechazo equivalente).
- Aviso de afiliación si hay links monetizados (FTC).
- Términos de servicio que limiten responsabilidad y describan el servicio como es.
- Datos recolectados: inventario escrito (qué, dónde vive, cuánto se retiene) — "no sé qué guardamos" es el peor estado posible.

## 3. Protocolo de corrección (patrón del reel — prompt de auditoría)

Cuando reviso una app (propia o de cliente): (1) inventariar qué puntos 1-6 aplican; (2) para cada uno, verificación PROGRAMÁTICA cuando sea posible (grep de `fonts.googleapis.com` en el repo, curl al footer buscando unsubscribe, inspección del flujo de registro); (3) producir el diff/corrección por punto con evidencia; (4) entregar tabla: punto → estado (cumple/rompe/fixed) → evidencia. Apps de cliente: la tabla es el entregable — implementa primero (regla 2 del núcleo), no un "deberías".

## 4. Señales de alarma específicas del ecosistema IA

- Landing generada con plantilla que incluye Google Fonts por defecto (casi todas las generan así).
- Widgets de analytics/replay añadidos "para ver qué pasa" sin política ni máscara.
- Formularios de beta que recolectan emails sin aviso de uso.
- Apps de usuarios-generated-content sin agente DMCA (patrón: clonar una idea = heredar también sus obligaciones).
- Suscripciones añadidas a último momento con Stripe checkout "pelado" (sin términos de renovación visibles).

## 5. Grader

- Cualquier app entregada/publicada lleva la tabla de 6 puntos con evidencia por fila → PASS.
- `grep -r "fonts.googleapis"` en el repo público de una app entregada sin justificación self-host → FAIL.
- Email de marketing sin unsubscribe + dirección postal → FAIL (bloquea el envío, guardarraíl).
- Checkout de suscripción sin términos de renovación visibles cerca del botón → FAIL.
- Deuda legal detectada y no reportada al founder en la misma sesión → FAIL grave.

## Grader (regla 28)

```bash
test_cumplimiento-legal-vibecoding() {
    # 1. Skill existe con frontmatter
    test -f 02_skills/cumplimiento-legal-vibecoding/SKILL.md
    # 2. Frontmatter tiene name y description
    grep -q "^name:" 02_skills/cumplimiento-legal-vibecoding/SKILL.md
    grep -q "^description:" 02_skills/cumplimiento-legal-vibecoding/SKILL.md
    # 3. Skill indexada en §12 del núcleo
    grep -q "cumplimiento-legal-vibecoding" 01_nucleo/ZOLO_V6.md
}
```
