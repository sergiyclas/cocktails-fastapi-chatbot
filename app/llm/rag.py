import asyncio
from langchain_openai import OpenAIEmbeddings
from app.database.orm_query import FaissVectorDB, SQLiteDB
from config import OPENAI_API_KEY, SQLITE_DB_PATH

LIMIT = 5

class CocktailRAG:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=OPENAI_API_KEY)
        self.vector_store = FaissVectorDB()
        self.sqlite_db = SQLiteDB(SQLITE_DB_PATH)

    async def get_relevant_cocktails(self, query: str, filters=None):
        filters = filters or {}

        similar_cocktail_ids = self.vector_store.search_similar_cocktails(query_ingredients=query, top_k=LIMIT)

        if not similar_cocktail_ids:
            print("Не знайдено коктейлів за запитом.")
            return []

        results = []
        for cocktails in similar_cocktail_ids:
            cocktail_id = cocktails['id']
            cocktail_info = self.sqlite_db.get_cocktail_by_id(cocktail_id)

            if cocktail_info:
                cocktail_data = {
                    "id": cocktail_info.id,
                    "name": cocktail_info.name,
                    "category": cocktail_info.category,
                    "alcoholic": cocktail_info.alcoholic,
                    "glassType": cocktail_info.glassType,
                    "instructions": cocktail_info.instructions,
                    "ingredients": cocktail_info.ingredients.split(","),
                    "ingredientMeasures": cocktail_info.ingredientMeasures.split(","),
                }
                results.append(cocktail_data)
            else:
                print(f"Не знайдено коктейль: ID {cocktail_id}")

        return results


if __name__ == "__main__":
    rag = CocktailRAG()
    results = asyncio.run(rag.get_relevant_cocktails("Find cocktails with Vodka"))
    print(f"Результати пошуку:")
    for cocktail in results:
        print(f"{cocktail['name']} - {cocktail['category']}, {cocktail['ingredients']} ({cocktail['alcoholic']})")
