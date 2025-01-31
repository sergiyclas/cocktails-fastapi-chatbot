from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import SQLITE_DB_PATH

from pydantic import BaseModel
from typing import List


class Model(BaseModel):
    pass

# Pydantic-модель для користувацьких вподобань
class UserMemorySchema(Model):
    user_id: str
    favorite_ingredients: List[str]

# Pydantic-модель для коктейлів
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

Base = declarative_base()

# Таблиця збереження вподобань користувачів
class UserMemory(Base):
    __tablename__ = "user_memories"
    user_id = Column(String, primary_key=True)
    favorite_ingredients = Column(Text)

# Таблиця для коктейлів
class Cocktail(Base):
    __tablename__ = "cocktails"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    alcoholic = Column(String)
    category = Column(String)
    glassType = Column(String)
    instructions = Column(Text)
    drinkThumbnail = Column(String)
    ingredients = Column(Text)
    ingredientMeasures = Column(Text)

# Підключення до бази
engine = create_engine(f"sqlite:///{SQLITE_DB_PATH}", echo=True)
SessionLocal = sessionmaker(bind=engine)

# Ініціалізація БД
def init_db():
    Base.metadata.create_all(bind=engine)

init_db()
