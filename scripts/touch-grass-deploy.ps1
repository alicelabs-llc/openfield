# ============================================================
# TOUCH GRASS — Deploy completo a GitHub + dev.to
# ============================================================
# Este script:
# 1. Crea el repo en GitHub
# 2. Clona, copia archivos, commit, push
# 3. Abre dev.to para crear el post
# ============================================================

$ErrorActionPreference = "Stop"
$repoName = "touch-grass"
$ghUser = "eddyflores100-lang"
$workspace = "C:\Users\Usuario\touch-grass-deploy"

Write-Host "🌿 Touch Grass — Deploy a GitHub + dev.to" -ForegroundColor Cyan
Write-Host ""

# 1. Crear repo en GitHub
Write-Host "→ Creando repo $repoName en GitHub..." -ForegroundColor Cyan
gh repo create $repoName --public --description "🌿 Verified field notes from your hike — open-source AI + cryptographic sealing (Hacktoberfest 2026 Week 1)" 2>$null
Write-Host "  ✅ Repo creado (o ya existe)" -ForegroundColor Green

# 2. Clonar
New-Item -ItemType Directory -Path $workspace -Force | Out-Null
Set-Location $workspace
if (Test-Path touch-grass) { Remove-Item touch-grass -Recurse -Force }
gh repo clone $ghUser/$repoName touch-grass
Set-Location touch-grass

# 3. Copiar archivos del sandbox (el usuario debe tener los archivos en una carpeta)
Write-Host "→ Copiando archivos..." -ForegroundColor Cyan

# Crear estructura de directorios
New-Item -ItemType Directory -Path "src" -Force | Out-Null
New-Item -ItemType Directory -Path "photos" -Force | Out-Null
New-Item -ItemType Directory -Path "output" -Force | Out-Null
New-Item -ItemType Directory -Path "docs" -Force | Out-Null

Write-Host "  ⚠️  Pega los archivos del proyecto en esta carpeta:" -ForegroundColor Yellow
Write-Host "     $PWD" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Archivos necesarios:" -ForegroundColor Yellow
Write-Host "    - README.md"
Write-Host "    - LICENSE"
Write-Host "    - DEV_POST.md"
Write-Host "    - requirements.txt"
Write-Host "    - .gitignore"
Write-Host "    - src/field_notes.py"
Write-Host "    - src/create_demo_photos.py"
Write-Host "    - src/run_demo.py"
Write-Host "    - photos/*.jpg (5 fotos demo)"
Write-Host "    - output/journal.aleth"
Write-Host "    - output/journal.md"
Write-Host ""
Write-Host "  Presiona Enter cuando hayas pegado los archivos..." -ForegroundColor Cyan
Read-Host

# 4. Commit y push
Write-Host "→ Haciendo commit..." -ForegroundColor Cyan
git add -A
git status
git commit -m "feat: touch grass — verified field notes from your hike

Hacktoberfest 2026 DEV Challenge Week 1: Touch Grass.

A CLI tool that turns outdoor photos into a cryptographically verified
field journal using local open-source AI (Gemma 3n via Ollama) and
alethech's Ed25519-signed .aleth containers."

Write-Host "→ Empujando a GitHub..." -ForegroundColor Cyan
git push -u origin main

Write-Host ""
Write-Host "✅ Repo subido: https://github.com/$ghUser/$repoName" -ForegroundColor Green

# 5. Abrir dev.to para crear post
Write-Host ""
Write-Host "→ Abriendo dev.to para crear post..." -ForegroundColor Cyan
Start-Process "https://dev.to/new"

Write-Host ""
Write-Host "📋 COPIA EL SIGUIENTE TEXTO EN dev.to:" -ForegroundColor Yellow
Write-Host ""

# Imprimir el contenido del DEV_POST.md
$devPost = Get-Content "$PWD\DEV_POST.md" -Raw -ErrorAction SilentlyContinue
if ($devPost) {
    Write-Host $devPost
} else {
    Write-Host "(DEV_POST.md no encontrado — pega el contenido manualmente)"
}

Write-Host ""
Write-Host "Tags: #devchallenge #hf26challenge #hacktoberfest #touchgrass" -ForegroundColor Yellow
Write-Host ""
Write-Host "✅ Todo listo. Submit cuando termines." -ForegroundColor Green
