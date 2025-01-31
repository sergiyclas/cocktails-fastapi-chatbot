from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database.schema_sqlite import Base, UserMemory, Cocktail, ChatHistory
from app.database.model_sqlite import UserMemorySchema, CocktailSchema
import os
import json
import asyncio
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from config import FAISS_INDEX_PATH, DATASET_PATH, OPENAI_API_KEY, SQLITE_DB_PATH


class SQLiteDB:
    def __init__(self, SQLITE_DB_PATH):
        is_new_db = not os.path.exists(SQLITE_DB_PATH)
        self.engine = create_engine(f"sqlite:///{SQLITE_DB_PATH}", echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine)

        if is_new_db:
            print("Створення нової бази даних...")
            self.create_tables()
            self.populate_cocktail_table()
        else:
            print("База даних вже існує. Заповнення `cocktails` не потрібно.")

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def populate_cocktail_table(self):
        with self.SessionLocal() as db:
            if db.query(Cocktail).first():
                print("Таблиця `cocktails` вже заповнена.")
                return

            print("Завантаження коктейлів з файлу...")
            if not os.path.exists(DATASET_PATH):
                print(f"Файл {DATASET_PATH} не знайдено!")
                return

            df = pd.read_csv(DATASET_PATH)

            df["ingredients"] = df["ingredients"].apply(lambda x: json.dumps(eval(x)) if isinstance(x, str) else "[]")
            df["ingredientMeasures"] = df["ingredientMeasures"].apply(
                lambda x: json.dumps(eval(x)) if isinstance(x, str) else "[]")

            cocktails = [
                Cocktail(
                    id=row["id"],
                    name=row["name"],
                    alcoholic=row["alcoholic"],
                    category=row["category"],
                    glassType=row["glassType"],
                    instructions=row["instructions"],
                    drinkThumbnail=row["drinkThumbnail"],
                    ingredients=row["ingredients"],
                    ingredientMeasures=row["ingredientMeasures"],
                )
                for _, row in df.iterrows()
            ]

            db.add_all(cocktails)
            db.commit()
            print("Таблиця `cocktails` успішно заповнена!")

    def add_user_memory(self, user_memory: UserMemorySchema):
        with self.SessionLocal() as db:
            db_memory = UserMemory(user_id=user_memory.user_id, favorite_ingredients=",".join(user_memory.favorite_ingredients))
            db.merge(db_memory)
            db.commit()

    def get_user_memory(self, user_id: str):
        with self.SessionLocal() as db:
            memory = db.query(UserMemory).filter(UserMemory.user_id == user_id).first()
            return memory.favorite_ingredients.split(",") if memory else []

    def add_cocktail(self, cocktail: CocktailSchema):
        with self.SessionLocal() as db:
            db_cocktail = Cocktail(
                id=cocktail.id,
                name=cocktail.name,
                alcoholic=cocktail.alcoholic,
                category=cocktail.category,
                glassType=cocktail.glassType,
                instructions=cocktail.instructions,
                drinkThumbnail=cocktail.drinkThumbnail,
                ingredients=",".join(cocktail.ingredients),
                ingredientMeasures=",".join(cocktail.ingredientMeasures)
            )
            db.merge(db_cocktail)
            db.commit()

    def get_cocktail_by_id(self, cocktail_id: int):
        with self.SessionLocal() as db:
            return db.query(Cocktail).filter(Cocktail.id == cocktail_id).first()

    def save_chat_history(self, user_id: str, messages: list):
        with self.SessionLocal() as db:
            json_messages = json.dumps(messages)  # Перетворюємо список у JSON
            existing_history = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).first()
            if existing_history:
                existing_history.messages = json_messages
            else:
                new_history = ChatHistory(user_id=user_id, messages=json_messages)
                db.add(new_history)
            db.commit()

    def load_chat_history(self, user_id: str):
        with self.SessionLocal() as db:
            history = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).first()
            return json.loads(history.messages) if history else []

    def get_chat_history_as_json(self, user_id: str):
        messages = self.load_chat_history(user_id)
        return [
            {
                "role": msg["role"],
                "timestamp": msg.get("timestamp", ""),
                "content": msg.get("content", "No content available")  # ✅ Фікс: Заповнюємо порожні повідомлення
            }
            for msg in messages
        ] if messages else []

    def add_chat_message(self, user_id: str, role: str, content: str):
        with self.SessionLocal() as session:
            chat_record = session.query(ChatHistory).filter(ChatHistory.user_id == user_id).first()
            new_message = {"role": role, "content": content}

            if chat_record:
                history = json.loads(chat_record.messages)
                history.append(new_message)
                chat_record.messages = json.dumps(history)
            else:
                chat_record = ChatHistory(user_id=user_id, messages=json.dumps([new_message]))
                session.add(chat_record)

            session.commit()

    def get_chat_history(self, user_id: str):
        with self.SessionLocal() as session:
            chat_record = session.query(ChatHistory).filter(ChatHistory.user_id == user_id).first()
            if chat_record:
                return json.loads(chat_record.messages)  # Повертає JSON історію повідомлень
            return []  # Порожній масив, якщо історії немає



    def clear_chat_history(self, user_id: str):
        with self.SessionLocal() as db:
            db.query(ChatHistory).filter(ChatHistory.user_id == user_id).delete()
            db.commit()


class FaissVectorDB:
    def __init__(self, dataset_path=DATASET_PATH, faiss_index_path=FAISS_INDEX_PATH):
        self.dataset_path = dataset_path
        self.faiss_index_path = faiss_index_path
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=OPENAI_API_KEY)
        self.vector_store = None
        self.load_or_create_index()

    def load_or_create_index(self):
        if os.path.exists(os.path.join(self.faiss_index_path, "index.faiss")) and os.path.exists(os.path.join(self.faiss_index_path, "index.pkl")):
            print("Завантаження існуючого FAISS-індексу через Langchain...")
            self.vector_store = FAISS.load_local(
                self.faiss_index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            print("FAISS-індекс не знайдено, створюємо новий...")
            asyncio.run(self.add_cocktails_to_index())

    async def add_cocktails_to_index(self):
        print("Додавання коктейлів у FAISS...")

        df = pd.read_csv(self.dataset_path)

        docs = []
        metadatas = []
        for _, cocktail in df.iterrows():
            text = f"{cocktail['name']} - {cocktail['category']} - {cocktail['alcoholic']} - {cocktail['ingredients']}"
            docs.append(text)
            metadatas.append({
                "id": cocktail["id"],
                "name": cocktail["name"],
                "category": cocktail["category"],
                "alcoholic": cocktail["alcoholic"],
                "glassType": cocktail["glassType"],
                "instructions": cocktail["instructions"],
                "ingredients": cocktail["ingredients"],
                "ingredientMeasures": cocktail["ingredientMeasures"]
            })

        self.vector_store = FAISS.from_texts(docs, self.embeddings, metadatas=metadatas)

        self.vector_store.save_local(self.faiss_index_path)
        print("FAISS-індекс збережено")

    def search_similar_cocktails(self, query_ingredients, top_k=5):
        if not self.vector_store:
            print("FAISS-індекс не завантажено!")
            return []

        query_text = ', '.join(query_ingredients)
        results = self.vector_store.similarity_search(query_text, k=top_k)

        cocktail_data = []
        for res in results:
            cocktail_data.append(res.metadata)

        return cocktail_data


if __name__ == "__main__":
    sqlite_db = SQLiteDB(SQLITE_DB_PATH)
    faiss_db = FaissVectorDB()
    search_results = faiss_db.search_similar_cocktails(["Sugar"])

    for cocktail in search_results:
        print(f"{cocktail['name']} - {cocktail['category']} {cocktail['ingredients']} ({cocktail['alcoholic']})")
