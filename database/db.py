# Импорт библиотек
import aiosqlite
from pyexpat.errors import messages


# Функция для подключения к базе данных
async def create_connection():
    return await aiosqlite.connect('shop.db')

# Функция для создания таблицы пользователей (если не существует)
async def create_user_table():
    conn = await create_connection()
    cursor = await conn.cursor()
    await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users
                    (telegram_id INTEGER PRIMARY KEY,
                    email TEXT,
                    phone INTEGER)''')
    await conn.commit()
    await conn.close()

# Проверка, зарегистрирован ли пользователь
async def check_user_exists(user_id):
    conn = await create_connection()
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM users WHERE telegram_id=?", (user_id,))
    user = await cursor.fetchone()
    await conn.close()
    return user is not None

# Сохранение данных пользователя в базе данных
async def save_user_data(user_id, email, phone):
    print(f"Сохраняем данные: user_id={user_id}, email={email}, phone={phone}")
    conn = await create_connection()
    cursor = await conn.cursor()
    # Если телефон не передан, вставляем только email
    if email is not None and phone is None:
        await cursor.execute("INSERT INTO users (telegram_id, email) VALUES (?,?)", (user_id, email))
    # Если телефон передан, вставляем оба поля
    elif email is None and phone is not None:
        await cursor.execute("INSERT INTO users (telegram_id, email, phone) VALUES (?,?,?)", (user_id, email, phone))
    await conn.commit()
    await conn.close()

# Сохранение обновленых данных пользователя в базе данных
async def update_user_data(user_id, email, phone):
    conn = await create_connection()
    cursor = await conn.cursor()
    if email:
        await cursor.execute("UPDATE users SET email=? WHERE telegram_id=?", (email, user_id))
    elif phone:
        await cursor.execute("UPDATE users SET phone=? WHERE telegram_id=?", (phone, user_id))
    await conn.commit()
    await conn.close()