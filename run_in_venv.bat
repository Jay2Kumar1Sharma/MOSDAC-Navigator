@echo off
TITLE MOSDAC AI Bot Launcher (for Virtual Environments)

ECHO =================================================================
ECHO  MOSDAC AI Help Bot - VENV Launcher
ECHO =================================================================
ECHO.

REM Check if the virtual environment is activated by looking for a specific variable.
IF NOT DEFINED VIRTUAL_ENV (
    ECHO ***************************************************************
    ECHO * ERROR: Virtual Environment is NOT Activated!                *
    ECHO ***************************************************************
    ECHO.
    ECHO Please activate your virtual environment first by running:
    ECHO.
    ECHO   venv\Scripts\activate
    ECHO.
    ECHO Then, run this script again from this same command prompt.
    ECHO.
    PAUSE
    EXIT /B 1
)

ECHO VENV check passed. Your virtual environment '%VIRTUAL_ENV%' is active.
ECHO.

ECHO [1/4] Installing/verifying Python packages in your VENV...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: Failed to install Python packages.
    PAUSE
    EXIT /B 1
)
ECHO.

ECHO [2/4] Scraping the MOSDAC website. This may take several minutes...
cd mosdac_scraper
scrapy crawl mosdac -o scraped_data.jsonl
cd ..
ECHO.

ECHO [3/4] Building the AI's knowledge base...
IF EXIST vector_store (
    ECHO    - Deleting old knowledge base...
    rd /s /q vector_store
)
ECHO    - Processing scraped data and creating new vector store...
python backend/data_ingestion.py
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: Failed to build the vector store. Check logs above.
    PAUSE
    EXIT /B 1
)
ECHO.

ECHO [4/4] Starting application...
ECHO    - Launching backend server in the background...
START "MOSDAC_Backend" /B python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000

ECHO    - Waiting for 5 seconds for backend to initialize...
timeout /t 5 /nobreak > NUL

ECHO    - Launching Streamlit frontend...
ECHO      Your browser should open with the application shortly.
ECHO.
streamlit run frontend/app.py

ECHO.
ECHO --- Application has been closed. ---
taskkill /F /FI "WINDOWTITLE eq MOSDAC_Backend" >nul 2>&1
PAUSE