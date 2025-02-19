# Импорт библиотек
import aiosqlite


# Функция для подключения к базе данных
async def create_connection():
    conn = await aiosqlite.connect("shop.db")
    cursor = await conn.cursor()
    await cursor.execute("PRAGMA foreign_keys = ON;")  # Включаем поддержку FOREIGN KEY
    return conn


# Функция для создания таблицы (если не существует)
async def create_user_table():
    conn = await create_connection()
    cursor = await conn.cursor()
    await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users
                    (user_id INTEGER PRIMARY KEY,
                    email TEXT,
                    phone INTEGER)''')
    await conn.commit()
    await conn.close()

async def create_product_table():
    conn = await create_connection()
    cursor = await conn.cursor()
    await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products(
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    photo TEXT,
                    category TEXT NOT NULL)''')
    # await add_products()
    await conn.commit()
    await conn.close()


async def create_cart_table():
    conn = await create_connection()
    cursor = await conn.cursor()

    await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cart
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL DEFAULT 1,
                        FOREIGN KEY (product_id) REFERENCES products(product_id))''')
    await conn.commit()
    await conn.close()
    


# Наполнение таблицы товаров
async def add_products():
    conn = await create_connection()
    cursor = await conn.cursor()
    # Удаляем старые товары (если это необходимо)
    await cursor.execute('DELETE FROM products')
    await cursor.execute('''INSERT INTO products(name, description, price, photo, category) VALUES 
                ("Ноутбук", "Мощный ноутбук для работы и игр", 79999.99, "image/laptop1.jpg", "Электроника"),
                ("Смартфон", "Современный смартфон с хорошей камерой", 49999.99, "image/phone1.jpg", "Электроника"),
                ("Кроссовки", "Удобные кроссовки для бега", 5999.99, "image/sneakers1.png", "Одежда");''')
    await conn.commit()
    await conn.close()



# Проверка, зарегистрирован ли пользователь
async def check_user_exists(user_id):
    conn = await create_connection()
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = await cursor.fetchone()
    await conn.close()
    return user is not None


# Сохранение данных пользователя в базе данных
async def save_user_data(user_id, email, phone):
    conn = await create_connection()
    cursor = await conn.cursor()
    if email and phone:
        await cursor.execute("INSERT INTO users (user_id, email, phone) VALUES (?, ?, ?)", (user_id, email, phone))
    elif email:
        await cursor.execute("INSERT INTO users (user_id, email) VALUES (?, ?)", (user_id, email))
    elif phone:
        await cursor.execute("INSERT INTO users (user_id, phone) VALUES (?, ?)", (user_id, phone))
    await conn.commit()
    await conn.close()


# Сохранение обновленых данных пользователя в базе данных
async def update_user_data(user_id, email, phone):
    conn = await create_connection()
    cursor = await conn.cursor()
    if email:
        await cursor.execute("UPDATE users SET email=? WHERE user_id=?", (email, user_id))
    elif phone:
        await cursor.execute("UPDATE users SET phone=? WHERE user_id=?", (phone, user_id))
    await conn.commit()
    await conn.close()


# Удаление данных пользователя
async def delete_user_data(user_id):
    conn = await create_connection()
    cursor = await conn.cursor()
    await cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    await conn.commit()
    await conn.close()