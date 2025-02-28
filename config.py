"""
Project-wide configuration constants
"""
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Database directory
DATABASE_DIR = PROJECT_ROOT / "database"
FAISS_DB_PATH = DATABASE_DIR / "faiss_db"

# Create necessary directories
DATABASE_DIR.mkdir(exist_ok=True)
