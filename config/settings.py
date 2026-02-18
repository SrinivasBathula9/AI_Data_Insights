import os
from pathlib import Path

# Base Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Database Configuration
DATABASE_PATH = BASE_DIR / "data.db"

# Scraper Configuration
DEFAULT_SCRAPE_URL = "https://finance.yahoo.com/"
PAGE_TIMEOUT = 60000  # 60 seconds

# Gemini Configuration
GEMINI_MODEL = "gemini-3-flash-preview"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAiBTZXXn6M4F_eCqdeTJwhR0BcA1NpoMI")

# Logging Configuration
LOG_LEVEL = "INFO"
