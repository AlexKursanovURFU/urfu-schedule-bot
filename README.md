# urfu-schedule-bot
Телеграм-бот для получения расписания занятий Уральского федерального университета (УрФУ). Бот предоставляет удобный доступ к расписанию групп и преподавателей прямо в Telegram.

```bach
# Запуск бота
poetry run bot

# Запуск тестов
poetry run pytest

# Запуск тестов с покрытием
poetry run pytest --cov=src --cov-report=term-missing

# Форматирование кода
poetry run black src tests

# Проверка сортировки импортов и форматирования
poetry run isort --check-only src tests && poetry run black --check src tests
```