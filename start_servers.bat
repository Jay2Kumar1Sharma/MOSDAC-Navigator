@echo off
TITLE MOSDAC AI Bot - Start Servers

ECHO =================================================================
ECHO  MOSDAC AI Help Bot - Server Launcher
ECHO =================================================================
ECHO.

REM Check if the virtual environment is activated
IF NOT DEFINED VIRTUAL_ENV (
    ECHO ***************************************************************
    ECHO * WARNING: Virtual Environment is NOT Activated!              *
    ECHO ***************************************************************
    ECHO.
    ECHO It is recommended to activate your virtual environment first:
    ECHO   venv\Scripts\activate
    ECHO.
    ECHO Press any key to continue anyway, or Ctrl+C to cancel...
    PAUSE >nul
    ECHO.
)

REM Check if vector store exists
IF NOT EXIST vector_store (
    ECHO ***************************************************************
    ECHO * WARNING: Vector store not found!                            *
    ECHO ***************************************************************
    ECHO.
    ECHO The knowledge base ^(vector_store^) does not exist.
    ECHO Please run 'run_in_venv.bat' or 'run.bat' first to build it.
    ECHO.
    ECHO Press any key to continue anyway, or Ctrl+C to cancel...
    PAUSE >nul
    ECHO.
)

ECHO [1/2] Starting backend server...
ECHO    - Launching backend server in the background...
START "MOSDAC_Backend" /B python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000

ECHO    - Waiting for 5 seconds for backend to initialize...
timeout /t 5 /nobreak > NUL

ECHO [2/2] Starting frontend...
ECHO    - Launching Streamlit frontend...
ECHO      Your browser should open with the application shortly.
ECHO.
streamlit run frontend/app.py

ECHO.
ECHO --- Application has been closed. ---
ECHO    - Stopping backend server...
taskkill /F /FI "WINDOWTITLE eq MOSDAC_Backend" >nul 2>&1
ECHO    - Servers stopped.
PAUSE
