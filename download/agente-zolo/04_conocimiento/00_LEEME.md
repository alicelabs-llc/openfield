# KIT DE VENTAS AliceLabs — Operado por agente (Task 120)

> Misión asignada por el founder (21-oct-2026): *"BUSCA TRABAJO, SE AGENTE DE TRABAJO, BUSCA COMO VENDER TODA LA TECNOLOGIA QUE TENEMOS... NECESITAMOS VENDER, INGRESOS URGENTES, COSAS REALES... BUSCA EN ESPECIAL AGENTES, VE DONDE PUEDES SUBIR TODO LO QUE TENEMOS, LO MINIMO DE INTERVENCION HUMANA"*.
> Gmail lo cubre OTRO agente: este kit no toca la bandeja de entrada; prepara campañas para que las ejecute **NEXUS COLD**.

## Contenido del kit

| Archivo | Qué resuelve | Uso |
|---|---|---|
| `01_INVENTARIO_ACTIVOS.md` | "Qué tecnología tenemos para vender" — todo lo verificable EN VIVO con HTTP codes y dónde está el dinero de cada activo | Fuente única de verdad del pitch. Ninguna cifra fuera de este archivo se usa en un correo |
| `02_OFERTAS_Y_PRECIOS.md` | "Qué vendemos y a qué precio" — 3 carriles: servicios (ingreso ya), producto UTA (ingreso recurrente), marketplace (ingreso por comisión/x402) | Cada campaña de NEXUS COLD vende UNA oferta de aquí |
| `03_REGISTRO_PLATAFORMAS.md` | "Dónde subir todo lo que tenemos" — destinos con URL exacta, requisito, bloqueo y prioridad | Checklist de publicación; se tacha al completar |
| `04_CAMPANA_NEXUS_COLD.md` | "Cómo atraemos clientes y agentes" — guardarrails de deliverability 2026, 4 segmentos, secuencias listas para enviar (EN/ES) | Copiar secuencia → cargar en NEXUS COLD → enviar |
| `05_PROTOCOLO_AGENTE_VENTAS.md` | "Operar al nivel agente con mínima intervención humana" — reglas, escalera de ejecución, KPIs, qué decide el agente solo | Se carga en cada BOOT de ventas |
| `06_OPORTUNIDADES_INMEDIATAS.md` | "Trabajo YA" — bounties, demanda freelance verificada, señales de mercado | Primera fuente de caja |

## Las 3 reglas de oro del kit

1. **CERO cifras muertas en un pitch.** Antes de enviar cualquier correo, cada número citado (71,198 skills, v4.2.0, endpoints) se re-verifica en vivo contra `marketnow.site` — regla 6 y regla 23 del paquete v3.2. Un número muerto mata la credibilidad del activo más vendible que tenemos (la confianza).
2. **Una oferta por correo, un CTA, texto plano.** Guardarrails de deliverability 2026 (MailReach, ago-2026): ≤80 correos fríos/día por dirección, 1 dirección por dominio, warm-up ≥15% del volumen. NEXUS COLD debe operar dentro de estos límites o quemamos el dominio.
3. **El dinero entra por 3 puertas en este orden:** (1) servicios productizados con demanda verificada (Upwork ya tiene categoría "MCP Server Developers", rates $20–150/hr), (2) publicación masiva en registries donde agentes y humanos nos descubren (la misma ruta que ya funcionó con alethech), (3) monetización nativa para agentes (x402 ya mueve $24.24M/mes; Cloudflare cobra llamadas MCP — encaja con `m2m-checkout`/`agent-hire` que YA existen en nuestra API v4.2.0).

## Estado de verificación (21-oct-2026, fuentes primarias)

- Verificado en vivo este task: endpoints de marketnow.site (health/skills/agents/atc/agent-protocol/agent.json), npm, PulseMCP (pausado), Opire, Algora, Upwork (categoría MCP), x402, MailReach. Citas con URL en cada archivo.
- Marcado `⚠️ VERIFICAR-EN-BOOT`: pasos cuyo flujo exacto no se pudo confirmar hoy (formularios que exigen sesión). El agente los verifica al ejecutar, nunca los asume.
- NEXUS COLD: declarado por el founder, **no aparece en el worklog** → se registra en el inventario como activo a documentar; su configuración (dominio envío, warm-up, volumen) es bloqueo TÚ.
