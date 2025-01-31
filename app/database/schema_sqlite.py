from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserMemory(Base):
    __tablename__ = "user_memories"
    user_id = Column(String, primary_key=True)
    favorite_ingredients = Column(Text)

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

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    messages = Column(Text, nullable=False)
