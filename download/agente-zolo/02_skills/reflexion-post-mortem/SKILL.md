---
name: reflexion-post-mortem
description: Post-mortem obligatorio tras fallo verificado (v5.0, Reflexion). Activar ANTES de corregir cualquier fallo propio: eval rojo, deploy roto, cifra muerta publicada, respuesta rechazada por la comunidad, credencial muerta por descuido, acción desperdiciada, grader que falla 2 veces. También al terminar un run con terminator T3 (progreso nulo).
---

# Reflexión tras fallo — pagar el fallo UNA vez (v5.0, M8)

Reflexion (seminal, verificado en la literatura de agentes): el rendimiento sube cuando el agente acumula lecciones verbales de sus FALLOS y las reutiliza, en lugar de repetir el intento con los mismos supuestos. En ZOLO esto ya ocurría informalmente (las 14 reglas de oro nacieron de costes reales); la regla 29 lo vuelve OBLIGATORIO y estructurado ANTES de la corrección.

## 1. Por qué ANTES de corregir

Corregir primero = el contexto del fallo se pierde (la ventana avanza) y la corrección ataca el SÍNTOMA. El post-mortem primero obliga a identificar la CAUSA RAÍZ con el fallo fresco, y la lección queda escrita para la próxima vez — en esta sesión y en las siguientes (memoria episódica, L3/L4).

## 2. Protocolo de 4 campos (obligatorio, regla 29)

```markdown
### POST-MORTEM <slug> — <fecha America/Guayaquil>
1. ESPERABA: <resultado que el plan predecía>
2. OBTUVE: <lo que pasó, con evidencia (HTTP/exit/grep — nunca "pareció")>
3. CAUSA RAÍZ: <el eslabón que falló — técnica, de proceso o de definición; si son varios, el primero de la cadena>
4. LECCIÓN: LECCIÓN: <1 frase grep-able, con acción> — ¿regla candidata? ¿eval nuevo? ¿skill candidata?
```

- Máximo ~10 líneas. Si no cabe en 10, la causa raíz no está identificada — afinar, no expandir.
- La línea `LECCIÓN:` es el formato grep-able: `grep -n "LECCIÓN:" worklog.md` = todas las lecciones del agente.

## 3. Clasificación de la causa raíz (evita el blame equivocado)

| Tipo | Señal | Destino de la lección |
|---|---|---|
| Técnica (script, API, parseo) | exit code / formato / límite de plataforma | regla de oro §3 + posible skill (regla 28) |
| De proceso (orden de pasos, falta de verificación previa) | el paso correcto existía pero se ejecutó tarde/nunca | regla de iniciativa §2 + eval de regresión |
| De definición (la regla era ambigua o inexistente) | el comportamiento correcto no estaba escrito | §15 protocolo completo (fricción → regla → eval) |
| De contexto (dato faltante/stale en la ventana) | decidí con información vieja o incompleta | skill `memoria-jerarquica` + checkpoint §17 |

## 4. Cierre del ciclo (3 destinos obligatorios de toda lección)

1. **Worklog**: post-mortem completo en el Stage Summary de la task (L3).
2. **Prevención**: regla candidata (§15) Y/O eval nuevo en EVALS.md (el fallo de hoy es el escenario E<siguiente> de mañana) Y/O skill candidata si el procedimiento corregido es repetible (regla 28).
3. **Estado**: commit alethech si hubo cambio de estado (regla 24).

Solo los 3 destinos juntos cierran el post-mortem. Corrección sin post-mortem = la deuda se paga doble (ya ocurrió: la misma clase de fallo cobró la renovación vencida de CF well-known y el worklog v1 con secretos en claro).

## 5. Relación con los otros mecanismos (qué usa cuándo)

| Situación | Mecanismo |
|---|---|
| Fricción del USUARIO (corrección, frustración, parte ignorada) | §15 mejora continua (ya existente) |
| Fallo VERIFICADO del propio agente | esta skill (regla 29) |
| Éxito repetible | skill `biblioteca-skills` (regla 28) |
| Patrón que ya existe como regla pero falló igual | el fallo es de PROCESO → post-mortem + eval, no regla duplicada |

## 6. Post-mortems ya pagados (memoria episódica viva — no repetir)

- Reset #3 perdió el filesystem → `/tmp/my-project` como memoria de emergencia + checkpoints externos (regla 24).
- Worklog v1 con PATs en claro → huella 4+4 (regla 16).
- Ban de outreach con patrón repetido → disciplina anti-ban §7 (el patrón repetido = ban garantizado).
- Task 114 perdido por sesión sin commit de cierre → commit de cierre OBLIGATORIO (regla 24).

## Grader (regla 28)

```bash
test_reflexion-post-mortem() {
    # 1. Skill existe con frontmatter
    test -f 02_skills/reflexion-post-mortem/SKILL.md
    # 2. Frontmatter tiene name y description
    grep -q "^name:" 02_skills/reflexion-post-mortem/SKILL.md
    grep -q "^description:" 02_skills/reflexion-post-mortem/SKILL.md
    # 3. Skill indexada en §12 del núcleo
    grep -q "reflexion-post-mortem" 01_nucleo/ZOLO_V6.md
}
```
