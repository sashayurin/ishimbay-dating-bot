import aiosqlite

DB_PATH = "users.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT,
            age INTEGER,
            gender TEXT,
            photo TEXT,
            is_approved INTEGER DEFAULT 0
        )
        """)
        await db.commit()
