import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "app\data")

SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", os.path.join(DATA_DIR, "cocktail.db"))
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", os.path.join(DATA_DIR, "faiss.index"))
DATASET_PATH = os.getenv("DATASET", os.path.join(DATA_DIR, "final_cocktails.csv"))
INTERFACE_DIR = os.path.join(BASE_DIR, "app", "interface")
INDEX_HTML_PATH = os.path.join(INTERFACE_DIR, "index.html")
CHAT_APP_TS_PATH = os.path.join(INTERFACE_DIR, "chat_app.ts")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")