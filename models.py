from typing import List

from sqlalchemy import JSON, Column, Integer, String, Text

from database import Base


class Recipe(Base):
    """Рецепт, хранящийся в базе данных."""

    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    views = Column(Integer, nullable=False, default=0)
    cooking_time = Column(Integer, nullable=False)
    ingredients: List[str] = Column(JSON, nullable=False)
    description = Column(Text, nullable=False)
