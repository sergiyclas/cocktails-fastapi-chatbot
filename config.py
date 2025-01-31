import os
from dotenv import load_dotenv

load_dotenv()

# Конфігурація для SQLite та FAISS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# SQLite БД
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", os.path.join(DATA_DIR, "cocktail.db"))

# FAISS База
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", os.path.join(DATA_DIR, "faiss.index"))
