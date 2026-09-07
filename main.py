from typing import Annotated, List

from fastapi import FastAPI, HTTPException, Path
from sqlalchemy.future import select

import models
import schemas
from database import async_session, engine

app = FastAPI(
    title="Кулинарная книга",
    description=(
        "Асинхронный API для просмотра и добавления рецептов. "
        "Открытие подробной информации увеличивает счётчик просмотров рецепта."
    ),
    version="1.0.0",
)


@app.on_event("startup")
async def startup() -> None:
    """Создать таблицы базы данных при запуске приложения."""

    async with engine.begin() as connection:
        await connection.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown() -> None:
    """Закрыть соединения с базой данных при остановке приложения."""

    await engine.dispose()


@app.get(
    "/recipes",
    response_model=List[schemas.RecipeListOut],
    summary="Получить список рецептов",
    description=(
        "Возвращает краткие данные всех рецептов. Рецепты отсортированы "
        "по убыванию количества просмотров, а при равном количестве "
        "просмотров — по возрастанию времени готовки."
    ),
    response_description="Отсортированный список рецептов",
)
async def get_recipes() -> List[models.Recipe]:
    """Вернуть все рецепты в порядке популярности и времени готовки."""

    async with async_session() as session:
        result = await session.execute(
            select(models.Recipe).order_by(
                models.Recipe.views.desc(),
                models.Recipe.cooking_time.asc(),
            )
        )
        return result.scalars().all()


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeOut,
    summary="Получить рецепт",
    description=(
        "Возвращает подробные данные выбранного рецепта "
        "и увеличивает количество его просмотров на один."
    ),
    response_description="Подробные данные рецепта",
    responses={404: {"description": "Рецепт не найден"}},
)
async def get_recipe(
    recipe_id: Annotated[
        int,
        Path(
            title="Идентификатор рецепта",
            description="Уникальный идентификатор запрашиваемого рецепта",
            gt=0,
            examples=[1],
        ),
    ],
) -> models.Recipe:
    """Вернуть подробные данные рецепта и учесть просмотр."""

    async with async_session() as session:
        result = await session.execute(
            select(models.Recipe).where(models.Recipe.id == recipe_id)
        )
        recipe = result.scalars().first()
        if recipe is None:
            raise HTTPException(status_code=404, detail="Рецепт не найден")

        recipe.views += 1
        await session.commit()
        return recipe


@app.post(
    "/recipes",
    response_model=schemas.RecipeOut,
    summary="Создать рецепт",
    description=(
        "Создаёт рецепт с нулевым количеством просмотров и возвращает "
        "сохранённые данные вместе с присвоенным идентификатором."
    ),
    response_description="Созданный рецепт",
)
async def create_recipe(recipe: schemas.RecipeIn) -> models.Recipe:
    """Сохранить новый рецепт в базе данных."""

    new_recipe = models.Recipe(**recipe.dict(), views=0)
    async with async_session() as session:
        async with session.begin():
            session.add(new_recipe)
    return new_recipe
