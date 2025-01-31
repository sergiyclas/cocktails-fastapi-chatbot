from pydantic import BaseModel
from typing import List

class Model(BaseModel):
    pass

class UserMemorySchema(Model):
    user_id: str
    favorite_ingredients: List[str]

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
