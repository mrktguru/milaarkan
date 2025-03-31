import sqlite3

def get_connection(db_path="milaarkan.db"):
    """Возвращает соединение с базой данных."""
    conn = sqlite3.connect(db_path)
    return conn

def create_tables():
    """Создает таблицы, если они еще не существуют."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        balance INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
