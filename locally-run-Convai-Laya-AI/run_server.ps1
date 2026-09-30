# PowerShell Launcher for Convai Laya AI Local Server
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Starting Convai Laya AI Local Decision Server" -ForegroundColor Cyan
Write-Host "  Interactive Swagger UI: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Activate virtual environment if available
if (Test-Path "..\.venv\Scripts\Activate.ps1") {
    Write-Host "[*] Activating parent virtual environment..." -ForegroundColor Gray
    & "..\.venv\Scripts\Activate.ps1"
} elseif (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "[*] Activating local virtual environment..." -ForegroundColor Gray
    & ".venv\Scripts\Activate.ps1"
}

Write-Host "[*] Launching Uvicorn on http://localhost:8000 ..." -ForegroundColor Green
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
