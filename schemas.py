from typing import List

from pydantic import BaseModel, Field


class RecipeBase(BaseModel):
    """Общие данные рецепта."""

    title: str = Field(
        ...,
        title="Название",
        description="Название блюда",
        min_length=1,
        max_length=200,
        example="Сырники",
    )
    cooking_time: int = Field(
        ...,
        title="Время готовки",
        description="Время приготовления блюда в минутах",
        gt=0,
        example=30,
    )


class RecipeIn(RecipeBase):
    """Данные для создания нового рецепта."""

    ingredients: List[str] = Field(
        ...,
        title="Ингредиенты",
        description="Список ингредиентов блюда",
        min_items=1,
        example=["творог", "яйцо", "мука"],
    )
    description: str = Field(
        ...,
        title="Описание",
        description="Пошаговое текстовое описание приготовления блюда",
        min_length=1,
        example="Смешайте ингредиенты и обжарьте сырники с двух сторон.",
    )


class RecipeListOut(RecipeBase):
    """Краткие данные рецепта для таблицы со списком рецептов."""

    id: int = Field(
        ...,
        title="Идентификатор",
        description="Уникальный идентификатор рецепта",
        example=1,
    )
    views: int = Field(
        ...,
        title="Количество просмотров",
        description="Сколько раз пользователи открывали рецепт",
        ge=0,
        example=10,
    )

    class Config:
        orm_mode = True


class RecipeOut(RecipeIn):
    """Подробные данные рецепта."""

    id: int = Field(
        ...,
        title="Идентификатор",
        description="Уникальный идентификатор рецепта",
        example=1,
    )

    class Config:
        orm_mode = True
