# GitLab Transcend — TODO for User (5 acciones, ~30 min total)

## ⚠️ Lo que NO puedo hacer automáticamente

1. **Mirror repo a GitLab.com** — Token GitLab caducó (HTTP 401). Necesitas crear uno nuevo.
2. **Grabar 3-min demo video** — No tengo capability de screen recording.
3. **Submit en Devpost** — Requiere tu sesión.

---

## ✅ Lo que YA está listo (no necesitas hacer nada)

- Código completo: https://github.com/eddyflores100-lang/alethech-agent-vault
- Commit `ef95d20` con integración GitLab (4 módulos + 30 tests)
- 41/41 tests pasando
- Slide HTML para video: `/home/z/my-project/alethech-agent-vault/docs/gitlab-transcend-demo.html`
- Texto Devpost listo: `/home/z/my-project/download/GITLAB_TRANSCEND_SUBMISSION.md`

---

## 🎬 ACCIÓN 1 — Grabar el video demo (15 min)

### Opción A: Slide HTML + Screen Recorder (más rápido)

1. **Abre el slide HTML** en tu navegador:
   ```
   file:///home/z/my-project/alethech-agent-vault/docs/gitlab-transcend-demo.html
   ```

2. **Ponlo en fullscreen** (botón ⛶ o tecla `F`)

3. **Abre tu screen recorder favorito**:
   - **OBS Studio** (gratis, recomendado) — https://obsproject.com
   - **Loom** (gratis hasta 5 min, web-based) — https://www.loom.com
   - **QuickTime** (Mac) — File → New Screen Recording
   - **Windows+G** (Windows 10/11) — Game Bar screen recording

4. **Graba la presentación avanzando con flecha derecha**, narrando cada slide. El slide tiene 11 slides, ~15 segundos cada uno = 2:45 min total. Perfecto para el límite de 3 min.

### Opción B: Demo en vivo con código real (más impresionante pero requiere setup)

Si tienes Docker instalado localmente:
```bash
git clone https://github.com/eddyflores100-lang/alethech-agent-vault
cd alethech-agent-vault
cp .env.example .env  # edit with Vultr API key or leave for mock mode
docker compose up
```
Abre http://localhost:8000, graba:
1. Submit task "audit this code and improve it"
2. Show the red warning box when sandbox blocks `pip install`
3. Run `alethech-verify --task-id <id>` and show the verification output
4. Show the MR template that gets created

### Subir el video
- Sube a YouTube como **Unlisted** (no público, no privado — Devpost necesita poder verlo)
- Copia la URL

---

## 🔧 ACCIÓN 2 — Crear GitLab token + mirror repo (5 min)

### Paso 1: Crear GitLab personal access token

1. Ve a https://gitlab.com/-/user_settings/personal_access_tokens
2. Click **Add new token**
3. Nombre: `alethech-agent-vault-mirror`
4. Expiration date: 1 semana (no necesita más)
5. Scopes: marca solo **`api`** y **`write_repository`**
6. Click **Create personal access token**
7. **Copia el token** (empieza con `glpat-`)

### Paso 2: Enviar el mirror (yo lo hago por ti)

Pásame el token en el chat con este formato:
```
gitlab-token: glpat-xxxxxxxxxxxxxxxxxxxx
```

Y yo ejecuto el script que YA tengo listo:
```bash
python3 /home/z/my-project/scripts/mirror_to_gitlab.py
```

El script automáticamente:
1. Verifica el token
2. Crea el proyecto `eddyflores100-lang/alethech-agent-vault` en GitLab.com (público, MIT)
3. Agrega git remote `gitlab` al repo local
4. Push el branch `main`
5. Te devuelve la URL pública del repo en GitLab

### Paso 2 alternativo (manual, si prefieres hacerlo tú):

```bash
# 1. Create project on GitLab.com (vía web UI):
#    https://gitlab.com/projects/new
#    - "Create blank project"
#    - Project name: alethech-agent-vault
#    - Visibility: Public
#    - Initialize with README: NO
#    - Create project

# 2. Add remote + push:
cd /home/z/my-project/alethech-agent-vault
git remote add gitlab https://gitlab.com/<tu-username>/alethech-agent-vault.git
git push gitlab main
```

---

## 📝 ACCIÓN 3 — Submit en Devpost (5 min)

1. Ve a https://gitlab-transcend.devpost.com
2. Click **"Submit a project"** (botón arriba a la derecha)
3. Click **"Start a new project"**

### Llena los campos:

- **Project name:** `alethech-agent-vault: Verifiable Agent Execution on GitLab Duo`
- **Short description:** `An agent runner that sandboxes execution and signs every step into a tamper-evident DAG. Submission for Path B (Bring Your Own), Supervised autonomy level.`
- **Project URL:** `https://github.com/eddyflores100-lang/alethech-agent-vault` (y marca "Open source")
- **Code repository URL:** `https://gitlab.com/<tu-username>/alethech-agent-vault` (después del mirror)
- **Video URL:** YouTube link del video que grabaste
- **Built with:** Marca `GitLab Duo Agent Platform`, `Docker`, `FastAPI`, `GitHub Copilot`
- **Tags:** `agent-safety`, `mcp`, `provenance`, `verifiable-execution`, `hackathon`

### Para "text description":

Abre el archivo:
```
/home/z/my-project/download/GITLAB_TRANSCEND_SUBMISSION.md
```

Copia toda la sección bajo **"## SUBMISSION TEXT"** y pégala en el campo "Text description" de Devpost.

### Path/Track selection:
- Select **Path B: Bring Your Own**
- Select **Supervised** autonomy level
- Marca **"Most Stages Covered"** si quieres optar al prize especial $5K

### Final:
- Click **"Submit"** (no "Save draft" — tiene que ser Submit final)
- Deadline: **Oct 27, 2026 @ 13:00 UTC**

---

## 📋 Checklist final

- [ ] Video grabado y subido a YouTube (Unlisted)
- [ ] GitLab token creado + mirror pushed
- [ ] Devpost submission completada con todos los campos
- [ ] Recibes confirmación por email

**Tiempo total estimado:** 25-30 min si todo va bien.

---

## 🆘 Si algo falla

- Si Devpost no acepta el video URL → prueba cambiar la privacidad a "Public" temporalmente
- Si GitLab push falla → verifica que el token tiene scope `write_repository`
- Si las pruebas de código fallan → ya pasan en mi entorno (41/41), debería funcionar
- Si necesitas ayuda en cualquier paso → pásame el error exacto y lo resolvemos

---

## ⏰ Tiempo restante

**Deadline: Oct 27, 2026 @ 13:00 UTC**

Hoy es Oct 24, ~02:00 UTC. Te quedan:
- 3 días = 72 horas
- Hoy: 22h restantes
- Oct 25: 24h
- Oct 26: 24h
- Oct 27: hasta 13:00 UTC = 13h

**Total: 83 horas**. Suficiente.
