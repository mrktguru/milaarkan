import aiosqlite
from datetime import datetime

DB_NAME = "milaarkan.db"


# ========== USERS ==========

async def get_user(telegram_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                name TEXT,
                birth_date TEXT,
                birth_time TEXT,
                birth_city TEXT,
                energy INTEGER DEFAULT 0
            )
        """)
        async with db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
            return await cursor.fetchone()


async def save_user_profile(telegram_id, name, birth_date, birth_time, birth_city):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                name TEXT,
                birth_date TEXT,
                birth_time TEXT,
                birth_city TEXT,
                energy INTEGER DEFAULT 0
            )
        """)
        await db.execute("""
            INSERT INTO users (telegram_id, name, birth_date, birth_time, birth_city)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                name=excluded.name,
                birth_date=excluded.birth_date,
                birth_time=excluded.birth_time,
                birth_city=excluded.birth_city
        """, (telegram_id, name, birth_date, birth_time, birth_city))
        await db.commit()


# ========== ENERGY ==========

async def get_user_energy(user_id: int) -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT energy FROM users WHERE telegram_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


async def update_user_energy(user_id: int, delta: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET energy = energy + ? WHERE telegram_id = ?", (delta, user_id))
        await db.commit()


# ========== ACTION TRACKING ==========

async def save_user_action(user_id: int, action: str, date: str = None, check_only: bool = False) -> bool:
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                date TEXT
            )
        """)
        await db.commit()

        async with db.execute(
            "SELECT id FROM user_actions WHERE user_id = ? AND action = ? AND date = ?",
            (user_id, action, date)
        ) as cursor:
            exists = await cursor.fetchone()

        if check_only:
            return bool(exists)

        if not exists:
            await db.execute(
                "INSERT INTO user_actions (user_id, action, date) VALUES (?, ?, ?)",
                (user_id, action, date)
            )
            await db.commit()
        return False
