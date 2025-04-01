import aiosqlite

DB_NAME = "data.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                name TEXT,
                birth_date TEXT,
                birth_time TEXT,
                birth_city TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await db.commit()

async def get_user(telegram_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
            return await cursor.fetchone()

async def save_user(telegram_id, name, birth_date, birth_time, birth_city):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT OR REPLACE INTO users (telegram_id, name, birth_date, birth_time, birth_city)
            VALUES (?, ?, ?, ?, ?)
        """, (telegram_id, name, birth_date, birth_time, birth_city))
        await db.commit()
