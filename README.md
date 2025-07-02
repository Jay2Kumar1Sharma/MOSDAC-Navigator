# 🛰️ MOSDAC AI Help Bot

An intelligent assistant for navigating MOSDAC (Meteorological and Oceanographic Satellite Data Archival Centre) data and services. This bot uses Retrieval-Augmented Generation (RAG) to provide accurate answers about MOSDAC based on scraped website content.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Features

- **Smart Q&A**: Ask questions about MOSDAC data, services, and procedures
- **RAG-Powered**: Uses retrieval-augmented generation for accurate, context-aware responses
- **Web Scraping**: Automatically scrapes MOSDAC website for up-to-date information
- **Modern UI**: Clean Streamlit interface for easy interaction
- **API Backend**: FastAPI backend for programmatic access
- **Vector Search**: FAISS-powered semantic search for relevant content retrieval

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   Google        │
│   Frontend      │◄──►│   Backend       │◄──►│   Gemini API    │
│   (Port 8501)   │    │   (Port 8000)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   FAISS Vector  │
                       │   Store +       │
                       │   Knowledge Base│
                       └─────────────────┘
                                ▲
                                │
                       ┌─────────────────┐
                       │   Scrapy Web    │
                       │   Scraper       │
                       └─────────────────┘
```

## 📦 Prerequisites

- **Python 3.8+**
- **Google AI API Key** ([Get one here](https://aistudio.google.com/app/apikey))
- **Internet connection** (for web scraping and API calls)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd mosdac-bot
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Create Environment File
Create a `.env` file in the project root:

```bash
# Copy the example file
copy .env.example .env
```

### 2. Add Your Google AI API Key
Edit the `.env` file:
```
GOOGLE_API_KEY=your_actual_google_ai_api_key_here
```

> **Get your API key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to create a free API key.

## 🎯 Usage

### Quick Start (Recommended)
Run the complete setup and launch:
```bash
# For virtual environments
run_in_venv.bat

# Or for system Python
run.bat
```

This will:
1. Install dependencies
2. Scrape MOSDAC website
3. Build the knowledge base
4. Start both backend and frontend servers

### Manual Steps

#### 1. Scrape Website Data
```bash
cd mosdac_scraper
scrapy crawl mosdac -o scraped_data.jsonl
cd ..
```

#### 2. Build Knowledge Base
```bash
python backend/data_ingestion.py
```

#### 3. Start Servers

**Option A: Use the launcher script**
```bash
start_servers.bat
```

**Option B: Manual startup**
```bash
# Terminal 1: Start backend
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000

# Terminal 2: Start frontend
streamlit run frontend/app.py
```

### 4. Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
mosdac-bot/
├── 📁 backend/                 # FastAPI backend
│   ├── api.py                 # Main API endpoints
│   ├── config.py              # Configuration settings
│   ├── data_ingestion.py      # Vector store creation
│   ├── knowledge_base.py      # FAISS vector search
│   └── llm_handler.py         # Google Gemini integration
├── 📁 frontend/               # Streamlit UI
│   └── app.py                 # Main frontend application
├── 📁 mosdac_scraper/         # Scrapy web scraper
│   ├── scrapy.cfg
│   └── mosdac_scraper/
│       ├── spiders/
│       │   └── mosdac_spider.py
│       └── ...
├── 📁 vector_store/           # Generated knowledge base
│   ├── index.faiss
│   └── index.pkl
├── 📄 requirements.txt        # Python dependencies
├── 📄 .env                    # Environment variables
├── 📄 run.bat                 # Full setup script
├── 📄 run_in_venv.bat         # Venv setup script
├── 📄 start_servers.bat       # Server launcher
└── 📄 README.md               # This file
```

## 🧪 Testing

### Test Google AI API
```bash
python test_gemini.py
```

### Test Simple API Connection
```bash
python test_simple.py
```

### Test Complete Integration
```bash
python test_api.py
```

## 🔧 Troubleshooting

### Common Issues

**1. "No module named 'config'" Error**
- Make sure you're running the backend as a module: `python -m uvicorn backend.api:app`
- Check that `__init__.py` files exist in the backend directory

**2. "GOOGLE_API_KEY not found" Error**
- Ensure `.env` file exists in project root
- Verify your API key is correctly set in `.env`
- Check the API key is valid at [Google AI Studio](https://aistudio.google.com/app/apikey)

**3. "Vector store not found" Error**
- Run the full setup: `run_in_venv.bat` or `run.bat`
- Or manually build: `python backend/data_ingestion.py`

**4. Import Errors with Virtual Environment**
- Ensure virtual environment is activated: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**5. Scrapy Connection Issues**
- Check internet connection
- Some networks may block web scraping - try from a different network

### Deprecation Warnings
If you see warnings about `convert_system_message_to_human`, these are harmless and have been fixed in the latest version.

