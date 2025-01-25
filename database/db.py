# Импорт библиотек

# Функция для подключения к базе данных
async def create_connection():
    return await aiosqlite.connect('shop.db')

# Функция для создания таблицы пользователей (если не существует)
async def create_user_table():
    async with create_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users
                        (telegram_id INTEGER PRIMARY KEY,
                        email TEXT,
                        phone TEXT)''')
        await conn.commit()

# Проверка, зарегистрирован ли пользователь
async def check_user_exists(user_id):
    async with create_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM users WHERE telegram_id=?", (user_id,))
        user = await cursor.fetchone()
        return user is not None