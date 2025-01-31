from fastapi import FastAPI
from app.routes.routes import chat_router
from app.database.orm_query import SQLiteDB, FaissVectorDB
from config import FAISS_INDEX_PATH, SQLITE_DB_PATH, DATASET_PATH

import uvicorn

sqlite_db = SQLiteDB(SQLITE_DB_PATH)
faiss_db = FaissVectorDB(DATASET_PATH, FAISS_INDEX_PATH)
faiss_db.add_cocktails_to_index()

app = FastAPI(title="Cocktail Advisor Chat")

app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8060)
