@echo off
@REM This script is made if windows is a prefered way to run operations

@REM Backend/ Startup
echo Starting FastAPI Backend..

cd /d "%~dp0..\Backend"

IF EXIST "..\venv\Scripts\activate.bat" (
    call "..\venv\Scripts\activate.bat"
)

start cmd /k "uvicorn Backend.main:app --reload"

@REM Frontend/ Startup
echo Starting Frontend...
cd /d "%~dp0..\Frontend"

start cmd /k "python -m http.server 3000"

pause