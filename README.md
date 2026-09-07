# Кулинарная книга: CI и линтеры

Код перенесён из `module_26_fastapi/homework`. Проект рассчитан на Python 3.11.
Реализованы исходные методы `GET /recipes`, `GET /recipes/{recipe_id}`
и `POST /recipes`. Документация API доступна по адресам `/docs` и `/redoc`.

## Установка и проверка

В PowerShell перейдите в папку с этим README и выполните:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-dev.txt
.\.venv\Scripts\python -m flake8 .
.\.venv\Scripts\python -m isort --check-only --diff --skip .venv .
.\.venv\Scripts\python -m black --check --diff .
.\.venv\Scripts\python -m mypy main.py database.py models.py schemas.py tests
.\.venv\Scripts\python -m pytest
```

Запуск приложения:

```powershell
.\.venv\Scripts\python -m uvicorn main:app --reload
```

SQLite создаёт `recipes.db` при запуске. Тесты используют отдельную временную
базу для каждого теста. Проверяются создание и чтение рецепта, счётчик
просмотров, сортировка, отсутствие рецепта и некорректные входные данные.

## GitHub Actions

Публичный репозиторий: https://github.com/vova0786/fastapi-recipes-ci.
Для сдачи используется GitHub Actions — разрешённая заданием альтернатива GitLab CI.
Конфигурация `.github/workflows/ci.yml` запускает pytest, flake8, isort, black
и mypy при каждом push в любую ветку и при создании или обновлении Pull Request.
Пять результатов проверок доступны на вкладке Actions. Для Pull Request результаты также отображаются на вкладке Checks; перед слиянием все пять проверок должны завершиться успешно.

Для проверки Pull Request создайте ветку, внесите изменение в README,
отправьте ветку и откройте Pull Request в main. Дождитесь успешных проверок.
В настройках защиты ветки main включите обязательные проверки
pytest, flake8, isort, black и mypy перед слиянием.
Для сдачи отправьте ссылку на репозиторий и отметку «Сделано».

Конфигурация основана на документации:
https://docs.github.com/en/actions/tutorials/build-and-test-code/python.
