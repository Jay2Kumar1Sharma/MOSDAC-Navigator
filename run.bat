@echo off
TITLE MOSDAC AI Bot - Full Setup

ECHO =================================================================
ECHO  MOSDAC AI Help Bot - Complete Setup and Launch
ECHO =================================================================
ECHO.

REM Check if Python is available
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO ***************************************************************
    ECHO * ERROR: Python is not installed or not in PATH!             *
    ECHO ***************************************************************
    ECHO.
    ECHO Please install Python 3.8+ and ensure it's in your PATH.
    ECHO Download from: https://www.python.org/downloads/
    ECHO.
    PAUSE
    EXIT /B 1
)

ECHO Python check passed.
ECHO.

ECHO [1/5] Installing/verifying Python packages...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: Failed to install Python packages.
    ECHO Try creating a virtual environment first:
    ECHO   python -m venv venv
    ECHO   venv\Scripts\activate
    ECHO   Then run this script again.
    PAUSE
    EXIT /B 1
)
ECHO.

ECHO [2/5] Checking environment configuration...
IF NOT EXIST .env (
    ECHO Creating .env file from template...
    copy .env.example .env
    ECHO.
    ECHO ***************************************************************
    ECHO * IMPORTANT: Please edit .env file and add your Google API key *
    ECHO ***************************************************************
    ECHO.
    ECHO 1. Open .env file in a text editor
    ECHO 2. Replace 'your_google_ai_api_key_here' with your actual API key
    ECHO 3. Get your API key from: https://aistudio.google.com/app/apikey
    ECHO.
    ECHO Press any key when you've updated the .env file...
    PAUSE >nul
    ECHO.
)

ECHO [3/5] Scraping the MOSDAC website. This may take several minutes...
cd mosdac_scraper
scrapy crawl mosdac -o scraped_data.jsonl
cd ..
ECHO.

ECHO [4/5] Building the AI's knowledge base...
IF EXIST vector_store (
    ECHO    - Deleting old knowledge base...
    rd /s /q vector_store
)
ECHO    - Processing scraped data and creating new vector store...
python backend/data_ingestion.py
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: Failed to build the vector store. Check logs above.
    ECHO Make sure your Google API key is correctly set in .env file.
    PAUSE
    EXIT /B 1
)
ECHO.

ECHO [5/5] Starting application...
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
ECHO    - Stopping backend server...
taskkill /F /FI "WINDOWTITLE eq MOSDAC_Backend" >nul 2>&1
ECHO    - Setup complete.
PAUSE
