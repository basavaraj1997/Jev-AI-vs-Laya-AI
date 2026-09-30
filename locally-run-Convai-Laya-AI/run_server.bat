@echo off
title Convai Laya AI - Local Swagger Server
echo ================================================================
echo   Starting Convai Laya AI Local Decision Server
echo   Interactive Swagger UI: http://localhost:8000/docs
echo ================================================================

cd /d "%~dp0"

REM Activate virtual environment if present in parent directory
if exist "..\.venv\Scripts\activate.bat" (
    echo [*] Activating parent virtual environment...
    call "..\.venv\Scripts\activate.bat"
) else if exist ".venv\Scripts\activate.bat" (
    echo [*] Activating local virtual environment...
    call ".venv\Scripts\activate.bat"
)

echo [*] Launching Uvicorn on http://localhost:8000 ...
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
