from pydantic import BaseModel
from typing import List

# Базовий клас Pydantic
class Model(BaseModel):
    pass

# ✅ Pydantic-модель для користувацьких вподобань
class UserMemorySchema(Model):
    user_id: str
    favorite_ingredients: List[str]

# ✅ Pydantic-модель для коктейлів
class CocktailSchema(Model):
    id: int
    name: str
    alcoholic: str
    category: str
    glassType: str
    instructions: str
    drinkThumbnail: str
    ingredients: List[str]
    ingredientMeasures: List[str]
