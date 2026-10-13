# ============================================================
# ALGORA — Setup completo en 3 pasos
# ============================================================
# Algora usa GitHub OAuth. Este script abre el navegador
# en la página correcta de Algora para que autorices con GitHub.
# ============================================================

Write-Host "=== ALGORA SETUP ===" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Abrir Algora para login con GitHub
Write-Host "Paso 1: Abriendo Algora en tu navegador..." -ForegroundColor Yellow
Write-Host "  Click en 'Sign in with GitHub'" -ForegroundColor Yellow
Write-Host "  Autoriza la app de Algora en GitHub" -ForegroundColor Yellow
Write-Host ""
Start-Process "https://algora.io"

Write-Host ""
Write-Host "Paso 2: Despues de iniciar sesion, completa tu perfil:" -ForegroundColor Yellow
Write-Host "  - Agrega tus skills (Python, Rust, TypeScript, C++)" -ForegroundColor Yellow
Write-Host "  - Agrega tu bio" -ForegroundColor Yellow
Write-Host "  - Conecta tu email para recibir notificaciones de bounties" -ForegroundColor Yellow
Write-Host ""

Write-Host "Paso 3: Buscar bounties disponibles:" -ForegroundColor Yellow
Write-Host "  - Ve a https://algora.io/bounties" -ForegroundColor Yellow
Write-Host "  - Filtra por tus lenguajes" -ForegroundColor Yellow
Write-Host "  - Comenta /attempt en issues que puedas resolver" -ForegroundColor Yellow
Write-Host ""

Write-Host "=== PERFIL GITHUB YA ACTUALIZADO ===" -ForegroundColor Green
Write-Host "  Bio: Open source contributor — Rust, Python, TypeScript, C++"
Write-Host "  Location: Ecuador"
Write-Host "  Blog: https://github.com/eddyflores100-lang/alethech"
Write-Host ""

Write-Host "=== PARA VERIFICAR BOUNTIES DESDE POWERSHELL ===" -ForegroundColor Cyan
Write-Host "  python3 verify_bounty.py <owner/repo> <issue_number> <github_token>"
Write-Host ""
