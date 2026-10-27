# UNDP-ECU-00982 — Guía paso a paso

> **Proceso:** Consultoría para el análisis territorial de los registros de violencia basada en género y el fortalecimiento de capacidades de los/as funcionarios/as que forman parte del Sistema local de Prevención y Erradicación de la Violencia contra la Mujer en los cantones Cuenca, Azogues y Morona.
>
> **Reference:** UNDP-ECU-00982 · **Process:** RFP (Request for Proposal) · **Quantum ID:** 50418
> **Posted:** 06-Oct-2026 · **Deadline:** 27-Oct-2026 · 19:00 GMT-4 (= **18h00 hora Ecuador**) — faltan ~3 días
> **Marco:** Proyecto 01003906 Iniciativa Spotlight (ONU Mujer + UE)
> **Beneficiario:** UNDP Ecuador

---

## ⚠️ Regla crítica del proceso

> *"Se solicita **no incluir** la propuesta económica en las secciones o documentos de la oferta técnica, ya que su **oferta será rechazada**."*

**La propuesta técnica y la económica van en archivos SEPARADOS.** Si mezclas precio dentro del PDF técnico, te descalifican automáticamente.

---

## Paso 1 — Registro en Quantum (si no lo tienes, ~30 min)

URL de registro exclusiva de este proceso (no uses la genérica):
```
https://estm.fa.em2.oraclecloud.com/fscmUI/redwood/supplier-registration/register-supplier/register-supplier-verification?id=TUW16eK6qcr758BAzgbOMoYCOHny7FmchTkUPHRpltKdniNLP99l0YMAtw%3D%3D&lang=es
```

Datos a preparar antes de registrarte (la LLC ecuatoriana):
- **RUC** de la LLC (Registro Único de Contribuyentes)
- **Razón social** completa como consta en el RUC
- **Dirección fiscal** Ecuador
- **Representante legal** (cédula + nombres completos)
- **Contacto técnico** (email + teléfono del que va a manejar Quantum)
- **Cuenta bancaria** (la pedirán después, no en registro)
- **Tipo de proveedor:** Persona jurídica (NO persona natural)
- **País:** Ecuador
- **Categorías UNSPSC** que aplican:
  - `80131601` Servicios de análisis estadístico
  - `80111604` Servicios de consultoría en tecnología de la información
  - `92131700` Servicios de desarrollo social

Después de enviar el formulario, UNDP valida en 24-48h. **Si ya te registraste antes, NO crees otro perfil — usa "forgot password"**.

---

## Paso 2 — Acceder al proceso específico

Login: http://supplier.quantum.partneragencies.org

Buscar el proceso por **Reference Number** `UNDP-ECU-00982` o por **nego_id** `50418`.

URL directa al proceso (requiere sesión iniciada):
```
https://procurement-notices.undp.org/view_negotiation_dlink.cfm?nego_id=50418
```

Documentos del proceso (requiere login en SharePoint primero, luego en Quantum):
```
https://procurement-notices.undp.org/sharepoint/login.cfm
https://undp.sharepoint.com/sites/Docs-Public/Procurement/Forms/AllItems.aspx?FilterField1=NegotiationNumber&FilterValue1=UNDP-ECU-00982
```

---

## Paso 3 — Descargar el pliego completo

En Quantum, dentro del proceso `UNDP-ECU-00982`, descarga:

1. **Instrucciones a los Oferentes (ITB)** — documento principal
2. **Términos de Referencia (TdR)** — describe exactamente qué entregables se esperan
3. **Formulario de Oferta Técnica** — plantilla a rellenar
4. **Formulario de Oferta Económica** — plantilla separada
5. **Anexos**: Declaración de integridad, declaración financiera, UNCRC, formulario de experiencia previa, atestados

Lee TdR de principio a fin. **El documento puede tener 30-60 páginas.** Identifica:
- Alcance geográfico: cantones Cuenca (Azuay), Azogues (Cañar), Morona (Morona Santiago)
- Perfil requerido: ¿pide experticia en análisis territorial / VBG / GIS / machismo de datos?
- Equipo mínimo: ¿cuántos consultores? ¿CV del team leader?
- Entregables y cronograma (típicamente 6-9 meses)
- Presupuesto estimado (si lo revelan en el ITB; a veces lo ocultan)

---

## Paso 4 — Indicar intención de participar (HOY)

> *"Indique si tiene intención de presentar una oferta creando un borrador de respuesta sin enviarla directamente en el sistema."*

En Quantum, dentro del proceso, crea un **Draft Response** (sin enviar). Esto:
1. Te notifica si el PNUD modifica los requisitos antes del deadline
2. Te aparece en tu dashboard
3. No compromete — puedes abandonar después

**Hacer esto HOY mismo** (24 oct) para no perderse actualizaciones.

⚠️ La ventana para hacer consultas al PNUD **ya cerró el 13 de octubre**. No puedes preguntar dudas ahora — debes inferir todo del pliego.

---

## Paso 5 — Preparar la propuesta técnica (2 días)

La LLC debe presentar una **propuesta técnica en español** que típicamente incluye (según ITB estándar del PNUD, confirma con el documento real):

### Secciones técnicas (archivo PDF #1)

1. **Carta de presentación** (formato del PNUD, firmada por representante legal)
2. **Comprender el problema** (3-5 páginas)
   - Marco conceptual de VBG (violencia basada en género) en Ecuador
   - Ley Orgánica Integral para Prevenir y Erradicar la Violencia contra las Mujeres (Ley 103)
   - El Sistema Local de Prevención (cantonal) según la Ley 103
   - El contexto de Cuenca, Azogues, Morona (estadísticas INEC, fiscalía, 911)
3. **Metodología propuesta** (8-12 páginas)
   - Análisis territorial de los registros (cómo los vas a obtener, limpiar, georreferenciar)
   - Tipos de datos: denuncias en Fiscalía, llamadas al 911, casos del Sistema Cantonal
   - Herramientas: Python (pandas, geopandas), QGIS, dashboards interactivos
   - **Diferenciador LLC:** tamper-evident provenance con alethech para auditoría de datos sensibles (protección de víctimas, anonimización irreversible, hashed identifiers). Esto es ÚNICO — ningún otro oferente tendrá esto.
   - Fortalecimiento de capacidades de funcionarios (talleres, materiales, mentoría)
4. **Plan de trabajo y cronograma** (Gantt 6-9 meses)
5. **Equipo propuesto** con CVs
   - Team Leader: especialista en VBG con maestría (10+ años exp)
   - Especialista en análisis territorial / GIS
   - Especialista en datos / Python (aquí entra Edison Flores como técnico de la LLC)
   - Especialista en capacitación / género
6. **Experiencia relevante** de la LLC (mínimo 3 proyectos similares, aunque pueden ser subcontratados o partnership con ONGs locales)
7. **Anexos administrativos**: declaración de integridad, UNCRC, no estar en lista de exclusión, etc.

### Sección económica (archivo PDF #2 — SEPARADO)

- **Formulario de oferta económica** del PNUD
- Desglose por entregable + cronograma de pagos
- Típicamente: 30% inicio, 30% entregable 1, 30% entregable 2, 10% cierre
- **No incluyas precios en la propuesta técnica** — descalificación automática

---

## Paso 6 — Lo que la LLC necesita conseguir URGENTE

Si la LLC no tiene expertos en VBG / género / análisis territorial, **forma una alianza** con una consultora local ecuatoriana especializada en género. La LLC aporta:
- El componente técnico: Python + análisis de datos + alethech provenance + dashboards
- El componente de capacitación técnica
- Infraestructura de auditoría de datos sensibles

La consultora aliada aporta:
- Experticia VBG (equipo con maestrías en género, trabajo social)
- Trabajo de campo en Cuenca, Azogues, Morona
- Relación con instituciones (Consejo Cantonal de Igualdad, Alcalde, etc.)

**Sugerencias de aliados potenciales en Ecuador:**
- Corporación Casa Materna (Cuenca)
- Fundación Tiamar (Cuenca)
- Colectivo Miriam (Quito)
- CONAMU (Consejo Nacional de las Mujeres, ya es entidad pública)
- CEPAM Ecuador

---

## Paso 7 — Subir la propuesta (antes de 27 oct 18h00 EC time)

1. Login en Quantum
2. Vas al proceso `UNDP-ECU-00982` → tu Draft Response
3. Sube los archivos PDF (técnicos + económicos por separado)
4. Verifica que cada archivo esté marcado correctamente (técnico/económico)
5. Click **Submit** (NO Submit Draft — Submit final)
6. Recibirás confirmación por email

---

## ⚠️ Riesgos honestos a considerar

1. **Ventana de consultas ya cerró (13 oct)** — si hay ambigüedad en el TdR, no puedes preguntar.
2. **Requiere alianza con experta VBG** — la LLC sola no califica para el team leader.
3. **3 días es muy poco** — preparación típica de RFP del PNUD toma 7-14 días.
4. **Match no es perfecto** — el pliego es consultoría social, no software. El componente técnico (análisis de datos + dashboards) es solo 30-40% del scope. El resto es trabajo social / género / capacitación.
5. **Pago tardío del PNUD** — típicamente 30-60 días después de aceptado cada entregable. La LLC necesita capital de trabajo.

**Recomendación:** Evalúa el TdR HOY. Si la alianza con una consultora VBG local es viable en 48h y el presupuesto esperado justifica el esfuerzo (>$30K para el componente LLC), ve adelante. Si el TdR pide cosas que la LLC no puede entregar con alianza rápida, **declina y prioriza otros leads del master report** (que tienen ROI más alto y son 100% remotos sin trabas administrativas).

---

## Contacto directo PNUD Ecuador (NO usar para enviar consultas después del 13 oct)

**Email:** licitaciones.ec@undp.org
**Nombre:** Unidad de Adquisiciones — PNUD Ecuador

*La ventana de consultas cerró. NO les escribas pidiendo aclaraciones — no responderán y tu oferta puede ser penalizada si intentas contactar fuera de canal.*
