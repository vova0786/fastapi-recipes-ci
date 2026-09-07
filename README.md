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

## Публикация в GitLab

Публикация и проверка удалённого pipeline требуют доступа к вашему аккаунту
GitLab. Выполните оставшиеся шаги самостоятельно:

1. На **gitlab.com** создайте пустой проект с видимостью **Public**,
   без начального README. Учебный gitlab.skillbox.ru для сдачи не подходит.
2. Скопируйте из этой папки в отдельную папку вне учебного репозитория
   `main.py`, `database.py`, `models.py`, `schemas.py`, `tests`,
   `requirements.txt`, `requirements-dev.txt`, `pyproject.toml`,
   `.flake8`, `.gitignore`, `.gitlab-ci.yml` и `README.md`.
   Не переносите `.venv`, кеши и файлы базы данных.
3. Откройте PowerShell в новой папке и выполните команды ниже,
   заменив `YOUR_LOGIN` и `YOUR_PROJECT` своими значениями:

   ```powershell
   git init -b main
   git add .
   git commit -m "Настроены линтеры и тесты FastAPI"
   git remote add origin https://gitlab.com/YOUR_LOGIN/YOUR_PROJECT.git
   git push -u origin main
   ```

4. В разделе **Build → Pipelines** проверьте успешность всех пяти заданий.
   Если задания ожидают исполнителя, включите доступный runner в
   **Settings → CI/CD → Runners**.
5. Создайте новую ветку, внесите изменение, отправьте ветку и откройте
   Merge Request. Проверьте, что CI запускается и для push, и для Merge Request.
6. В **Settings → Merge requests → Merge checks** включите
   **Pipelines must succeed**, чтобы нельзя было принять изменения
   с неуспешными проверками.
7. Убедитесь, что проект виден без авторизации. Отправьте ссылку на проект
   и отметку «Сделано» в форме сдачи задания.

`.gitlab-ci.yml` должен находиться в корне нового репозитория.
Все пять заданий выполняются для каждого push в любую ветку и каждого
Merge Request. Правила событий настроены согласно
[документации GitLab](https://docs.gitlab.com/ci/jobs/job_rules/).
Совместимость форматирования обеспечивают профиль `black` для isort,
длина строки 88 и исключение E203 для flake8 согласно
[документации Black](https://black.readthedocs.io/en/stable/guides/using_black_with_other_tools.html).
