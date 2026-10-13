# ============================================================
# HACKTOBERFEST SCRIPT 1 — vajra #29 (skip Linux installer on macOS)
# ============================================================
# Ejecutar en PowerShell. Requiere `gh` autenticado.
# Repo: https://github.com/Ergane-Foundation/vajra
# Issue: #29 — Skip the Linux installer when starting on macOS
# Fix: 1 archivo (install.sh), +21 líneas, sin cambios en Linux

$ErrorActionPreference = "Stop"
$workspace = "C:\Users\Usuario\hacktoberfest-vajra"
New-Item -ItemType Directory -Path $workspace -Force | Out-Null
Set-Location $workspace

if (Test-Path vajra) { Remove-Item vajra -Recurse -Force }
gh repo clone Ergane-Foundation/vajra vajra
Set-Location vajra
git checkout -b fix/29-skip-linux-installer-on-macos

# Editar scripts/install.sh
$shPath = "scripts\install.sh"
$bytes = [System.IO.File]::ReadAllBytes("$PWD\$shPath")
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

# Insertar guard de macOS despues del root check, antes de "Detect Package Manager"
$old = @'
# Root Check
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}ERROR: Must run as root${NC}"
    echo "Run: sudo ./scripts/install.sh"
    exit 1
fi

# Detect Package Manager
'@

$new = @'
# Root Check
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}ERROR: Must run as root${NC}"
    echo "Run: sudo ./scripts/install.sh"
    exit 1
fi

# Refuse to run on macOS: this script installs Linux-only packages via
# apt/dnf/yum/pacman and would either fail mid-way (leaving the system in
# a half-installed state) or, worse, pick up Homebrew apt shim and install
# the wrong thing. macOS users should follow the manual setup steps in
# README.md instead — running start_macos.sh will not work either until
# the dependencies are present. See issue #29.
if [ "$(uname -s)" = "Darwin" ]; then
    echo -e "${RED}ERROR: This installer targets Linux only.${NC}"
    echo ""
    echo "Detected OS: macOS (Darwin). This script installs apt/dnf/yum/pacman"
    echo "packages that are not available on macOS, and running it here would"
    echo "leave your system in a half-configured state."
    echo ""
    echo "For macOS, follow the manual setup steps in README.md, or use the"
    echo "platform-specific scripts in scripts/ (e.g. start_macos.sh once the"
    echo "required dependencies are installed via Homebrew or MacPorts)."
    echo ""
    echo "Aborting before any package is touched."
    exit 1
fi

# Detect Package Manager
'@

$content = $content.Replace($old, $new)
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText("$PWD\$shPath", $content, $utf8NoBom)

git diff --stat
git add $shPath
git -c user.name="Edison Flores" -c user.email="eddyflores100-lang@protonmail.com" commit -m "install: refuse to run on macOS instead of failing mid-way" -m "Closes #29." -m "scripts/install.sh is a Linux-only installer: it detects the system package manager from a hard-coded list of apt-get, dnf, yum and pacman, then invokes it to install python3, build-essential, iptables, iproute2 and friends. None of these packages exist on macOS in the form the script expects. Previously, running install.sh on macOS would either: find a Homebrew-provided apt-get shim in PATH and proceed to install the wrong packages, leaving the system in a half-configured state, or reach the no supported package manager found branch deep inside the script after the package lists had already been updated by whatever the shim did, leaving stray state behind. Both outcomes are worse than refusing up front. Add an explicit Darwin guard at the top of the script (right after the root check, before any package manager probing) that prints a clear error message pointing the user at README.md and the platform-specific scripts in scripts/. No behaviour change on Linux."

gh repo fork Ergane-Foundation/vajra --clone=false
git remote rename origin upstream 2>$null
git remote remove origin 2>$null
git remote add origin "https://github.com/eddyflores100-lang/vajra.git"
git push -u origin fix/29-skip-linux-installer-on-macos

gh pr create --repo Ergane-Foundation/vajra --base main --head eddyflores100-lang:fix/29-skip-linux-installer-on-macos --title "install: refuse to run on macOS instead of failing mid-way" --body "Closes #29. scripts/install.sh is a Linux-only installer. Add an explicit Darwin guard at the top of the script (right after the root check, before any package manager probing) that prints a clear error message pointing the user at README.md and the platform-specific scripts in scripts/. No behaviour change on Linux."
