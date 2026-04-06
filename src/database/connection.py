import sqlite3
from pathlib import Path

# Создаем папку для БД (если её нет)
DB_DIR = Path(__file__).parent.parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DB_DIR / "database.db"


def get_db_connection():
    """
    Создает и возвращает подключение к базе данных.

    Returns:
        sqlite3.Connection: Объект подключения к БД
    """
    return sqlite3.connect(DATABASE_PATH)


def init_db():
    """
    Инициализирует базу данных: создает таблицы, если они не существуют.

    Таблицы:
    - Users: хранит информацию о пользователях и их группах
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            group_title TEXT,
            course INTEGER,
            division_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()
    print("✅ База данных инициализирована")


# Автоматически создаем таблицы при импорте модуля
if __name__ != "__main__":
    init_db()