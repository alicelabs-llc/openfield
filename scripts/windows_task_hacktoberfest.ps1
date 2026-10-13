# Script para Windows PowerShell - ejecutar mañana 9am hora Ecuador
# Guardar en C:\Users\Usuario\hacktoberfest_runner.ps1
# Programar con Task Scheduler

$DATE = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "=== Hacktoberfest runner - $DATE ==="

# Verificar estado de los 5 MRs GitLab
$gitlabToken = "PEGAR_AQUI_TOKEN_NUEVO"
Write-Host ""
Write-Host "=== Estado MRs GitLab ==="

$mrs = @(
    @{ proj = "OpenMW%2Fopenmw"; iid = "5667"; name = "OpenMW !5667" }
    @{ proj = "inkscape%2Fextensions"; iid = "739"; name = "inkscape/extensions !739" }
    @{ proj = "inkscape%2Finkscape"; iid = "8203"; name = "inkscape !8203" }
    @{ proj = "fdroid%2Ffdroidclient"; iid = "1786"; name = "fdroidclient !1786" }
)

foreach ($mr in $mrs) {
    try {
        $resp = Invoke-RestMethod -Uri "https://gitlab.com/api/v4/projects/$($mr.proj)/merge_requests/$($mr.iid)" -Headers @{ Authorization = "Bearer $gitlabToken" } -TimeoutSec 10
        Write-Host "  $($mr.name): $($resp.state)"
    } catch {
        Write-Host "  $($mr.name): error - $($_.Exception.Message)"
    }
}

# Verificar PR GitHub dino #124
Write-Host ""
Write-Host "=== PR GitHub dino #124 ==="
gh pr view 124 --repo meetdino/dino --json state,mergedAt 2>&1

# Mostrar plan
Write-Host ""
Write-Host "=== Plan para hoy (ver HACKTOBERFEST_PLAN.md) ==="
Write-Host "1. Responder maintainer dino PR #124 (texto preparado)"
Write-Host "2. Atacar vajra issue #29 (skip Linux installer macOS)"
Write-Host "3. Atacar harbour issue #41 (filter control chars)"
Write-Host "4. Atacar Prism-platform issue #388 (md5 -> sha256)"
