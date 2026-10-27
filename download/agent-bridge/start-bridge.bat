@echo off
REM start-bridge.bat — One-click launcher for AliceLabs agent-bridge on Windows
REM Double-click this file to start the bridge server.
REM The server runs until you press Ctrl+C or close this window.

title AliceLabs agent-bridge
cd /d "%~dp0"

echo.
echo ===============================================
echo   AliceLabs agent-bridge - starting...
echo ===============================================
echo.

REM Check Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo    Install from https://www.python.org/downloads/
    echo    Remember to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)

REM Check config.json exists
if not exist "config.json" (
    echo ❌ config.json not found in %CD%
    echo    Make sure you extracted all files from the agent-bridge folder.
    echo.
    pause
    exit /b 1
)

REM Start the bridge
echo 🚀 Starting agent-bridge on http://127.0.0.1:7421
echo.
echo    Leave this window open. Open another PowerShell to run cloudflared:
echo      .\cloudflared.exe tunnel --url http://localhost:7421
echo.
echo    Press Ctrl+C to stop.
echo.

python agent-bridge.py

pause
