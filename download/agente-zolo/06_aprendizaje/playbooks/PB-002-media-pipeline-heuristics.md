# Playbook: PB-002 — Media pipeline: verificar firmas, fijar fps, textfile para drawtext

## Patrón detectado
Pipeline de generación de medios (audio→images→video) requiere 4 heurísticas específicas para no romper: verificar firma de binarios, fijar fps como filtro, usar textfile para drawtext, verificar feeds antes de config.

## Evidencia (4 ocurrencias)

- **2026-10-25** — Task 125-B — `api-imagenes-devuelve-jpeg`: API devuelve JPEG (JFIF) aunque contrato dice PNG. Sin verificar magic bytes, el pipeline rompe.
- **2026-10-25** — Task 125-B — `ffmpeg-concat-imagenes-duraciones`: "última imagen repetida" hereda duration y estira timeline; -r 30 como output duplica primera slide; -shortest inestable (77s vs 21s entre corridas).
- **2026-10-25** — Task 125-B — `drawtext-solo-textfile`: texto inline en drawtext rompe con tildes, comas, comillas, %.
- **2026-10-25** — Task 125-A — `fuentes-verificadas-antes-de-config`: 3 de 5 feeds RSS iniciales muertos en vivo (Infobae 404, El Universo 404, El Comercio anti-bot).

## Heurística portable

```
PARA PIPELINES DE MEDIOS (audio/images/video):

1. VERIFICAR FIRMA ANTES DE CONSUMIR
   - Cualquier archivo binario generado por API → verificar magic bytes
   - JPEG vs PNG: los primeros bytes dicen JFIF (JPEG) o ‰PNG (PNG)
   - Si no matchea el contrato → normalizar antes de procesar

2. FFMPG CONCAT DE IMÁGENES
   - Fijar fps como FILTRO de video: -vf fps=30 (NO como opción de output -r 30)
   - Capar duración con: -t <duración_audio+0.05>
   - NUNCA usar -shortest (inestable entre corridas)

3. DRAWTEXT CON TEXTO NO-ASCII
   - SIEMPRE usar textfile=<archivo_temporal> + expansion=none
   - NUNCA texto inline en el filtro (tildes, comas, comillas, % rompen)
   - El archivo temporal se escribe UTF-8 y se pasa como path

4. FEEDS/APIS EN CONFIG
   - Ninguna fuente entra a config sin verificación EN VIVO
   - Verificar: HTTP code + contenido parseable (JSON/XML/ RSS válido)
   - El sistema debe saltar feeds caídos sin tumbar el run (try/except + log)
   - Reemplazar inmediatamente feeds muertos con alternativas verificadas
```

## Acción de promoción

- [x] Promovido a regla de oro en skill `noticiero-matutino` (§6.2, §6.4, §6.5)
- [x] Eval E53 (etapas reanudables) cubre el patrón de pipeline
- [x] Eval E54 (firma de archivos) cubre el patrón de magic bytes
- [x] Eval E55 (fuentes verificadas) cubre el patrón de feeds
- [x] Playbook PB-001 cubre el patrón transversal "verificar en vivo antes de consumir"
- [x] Regla 34 del núcleo formaliza el patrón a nivel protocolo

## Contexto de origen

Generado por **skill auto-curador** (primera ejecución completa, Task 128).
Consolida 4 learnings del noticiero-matutino (Task 125) en un solo playbook.
4 ocurrencias detectadas en ledger → umbral de promoción (mínimo 2).

---

**Próxima revisión**: cuando se detecten 2+ ocurrencias más de este patrón (umbral 6 para auto-aplicación sin gate founder).
