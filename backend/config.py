from pathlib import Path
from dotenv import load_dotenv

# --- Load Environment Variables ---
# This line finds the .env file in the project root and loads its variables
# into the environment, making them accessible via os.getenv()
load_dotenv()

# --- Base Directory ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Data and Model Paths ---
MOSDAC_SCRAPER_DIR = BASE_DIR / "mosdac_scraper"
SCRAPED_DATA_FILE = MOSDAC_SCRAPER_DIR / "scraped_data.jsonl"
VECTOR_STORE_PATH = BASE_DIR / "vector_store"

# --- Model Configuration ---
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# --- API Configuration ---
API_HOST = "127.0.0.1"
API_PORT = 8000