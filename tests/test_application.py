from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import main


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    """Запускать каждый тест с отдельной временной базой данных."""
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'test.db'}")
    monkeypatch.setattr(main, "engine", engine)
    monkeypatch.setattr(
        main,
        "async_session",
        sessionmaker(engine, expire_on_commit=False, class_=AsyncSession),
    )
    with TestClient(main.app) as test_client:
        yield test_client


def test_create_and_read_recipe(client: TestClient) -> None:
    recipe = {
        "title": "Сырники",
        "cooking_time": 30,
        "ingredients": ["творог", "яйцо", "мука"],
        "description": "Смешайте ингредиенты и обжарьте.",
    }
    response = client.post("/recipes", json=recipe)
    assert response.status_code == 200
    created = response.json()
    assert created == {**recipe, "id": created["id"]}
    assert client.get("/recipes").json() == [
        {"id": created["id"], "title": "Сырники", "cooking_time": 30, "views": 0}
    ]
    for expected_views in (1, 2):
        response = client.get(f"/recipes/{created['id']}")
        assert response.status_code == 200
        assert response.json() == created
        assert client.get("/recipes").json()[0]["views"] == expected_views


def test_sort_recipes(client: TestClient) -> None:
    ids = []
    for cooking_time in (40, 20, 10):
        response = client.post(
            "/recipes",
            json={
                "title": f"Блюдо {cooking_time}",
                "cooking_time": cooking_time,
                "ingredients": ["вода"],
                "description": "Приготовить.",
            },
        )
        assert response.status_code == 200
        ids.append(response.json()["id"])
    assert client.get(f"/recipes/{ids[0]}").status_code == 200
    response = client.get("/recipes")
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [ids[0], ids[2], ids[1]]


def test_missing_recipe(client: TestClient) -> None:
    assert client.get("/recipes").json() == []
    response = client.get("/recipes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Рецепт не найден"}
    assert client.get("/recipes").json() == []


@pytest.mark.parametrize(
    ("field", "value"),
    [("title", ""), ("cooking_time", 0), ("ingredients", []), ("description", "")],
)
def test_invalid_recipe(client: TestClient, field: str, value: object) -> None:
    recipe: dict[str, object] = {
        "title": "Суп",
        "cooking_time": 10,
        "ingredients": ["вода"],
        "description": "Сварить.",
    }
    recipe[field] = value
    assert client.post("/recipes", json=recipe).status_code == 422
    assert client.get("/recipes").json() == []


@pytest.mark.parametrize("recipe_id", ["0", "-1", "abc"])
def test_invalid_recipe_id(client: TestClient, recipe_id: str) -> None:
    assert client.get(f"/recipes/{recipe_id}").status_code == 422
