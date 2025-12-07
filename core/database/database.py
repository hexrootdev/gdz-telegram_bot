import aiosqlite

database = 'Users.db'
async def create_database():
    async with aiosqlite.connect(database) as db:
        await db.execute('''CREATE Table IF NOT EXISTS Users (
                         id INTEGER PRIMARY KEY,
                         tg_id INTEGER,
                         class INTEGER
                         )
                         ''')
        await db.commit()

async def add_user(tg_id):
    async with aiosqlite.connect(database) as db:
        await db.execute('INSERT INTO Users (tg_id) VALUES (?)', (tg_id,))
        await db.commit()

async def add_class(class_, tg_id):
    async with aiosqlite.connect(database) as db:
        await db.execute('UPDATE Users SET class = ? WHERE tg_id = ?', (class_, tg_id,))
        await db.commit()

async def is_class(tg_id):
    async with aiosqlite.connect(database) as db:
        cursor = await db.execute('SELECT class FROM Users WHERE tg_id = ?', (tg_id,))
        cls = await cursor.fetchone()
        if cls == (None,):
            return False
        return True

async def get_class(tg_id):
    async with aiosqlite.connect(database) as db:
        cursor = await db.execute('SELECT class FROM Users WHERE tg_id = ?', (tg_id,))
        cls = await cursor.fetchone()
        return str(cls[0])