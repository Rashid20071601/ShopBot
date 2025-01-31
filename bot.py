# Импорт библиотек
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
import logging
import asyncio
from utils import misc
from config import *
from keyboards import inline, reply
from database import db


# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
user_category = {}  # Словарь для хранения категорий пользователей
categories = []  # Глобальный список для хранения категорий


async def on_startup(dp):
    """Подключение к базе данных при старте бота"""
    await db.create_user_table()
    await db.create_product_table()


'''=============================== ОБРАБОТЧИК КОМАНД ==============================================='''
'''================================================================================================='''

# -------------------------------------------------------------------------------------------------------
# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if await db.check_user_exists(user_id):
        await message.answer("Добро пожаловать в наш онлайн-магазин! 🛍️\nВведите /help для списка команд.")

    else:
        await message.answer("Добро пожаловать в наш онлайн-магазин! 🛍️\nМы начнем с регистрации. Введите ваш e-mail.")
        await UserRegistration.waiting_for_email.set()


# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer("Доступные команды:"
                        "\n/start - Начать"
                        "\n/help - Помощь"
                        "\n/update - Обновить или удалить данные"
                        "\n/catalog - Посмотреть каталог товаров")
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
# Обработчик команды /catalog для отображения категорий
@dp.message_handler(commands=['catalog'])
async def show_categories(message: types.Message):
    global categories
    conn = await db.create_connection()
    cursor = await conn.cursor()

    # Получаем уникальные категории
    categories = await cursor.execute("SELECT DISTINCT category FROM products")
    categories = await categories.fetchall()

    # Формируем кнопки с категориями
    category_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if categories:
        for category in categories:
            category_kb.add(category[0])
        await conn.close()
        await message.answer("Выберите категорию", reply_markup=category_kb)

    else:
        await message.answer("Категорий пока нет.")


# Обработчик выбора категории
@dp.message_handler(lambda message: any(category[0].lower() == message.text.strip().lower() for category in categories))
async def show_products_by_category(message: types.Message):
    category = message.text.strip()
    conn = await db.create_connection()
    cursor = await conn.cursor()

    # Проверяем, существует ли такая категория
    category_check = await cursor.execute("SELECT DISTINCT category FROM products WHERE category=?", (category,))
    category_check = await category_check.fetchone()  # Получаем одну строку

    if not category_check:   # Если ничего не найдено, значит категории нет
        await message.answer("Такой категории нет, выберите из списка.")
        await conn.close()
        return
    
    # Запоминаем выбранную категорию
    user_category[message.from_user.id] = category

    # Получаем товары из выбранной категории
    products = await cursor.execute("SELECT product_id, name, price FROM products WHERE category=?", (category,))
    products = await products.fetchall()
    await conn.close()
    if products:
        # Выводим товары в выбранной категории
        product_list = '\n'.join([f'{i+1}. {product[1]} - {product[2]} ₽' for i, product in enumerate(products)])
        await message.answer(f"Товары в категории '{category}': \n\n{product_list}", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Введите номер товара для подробностей.", reply_markup=inline.back_kb)

    else:
        await message.answer("В этой категории пока нет товаров.", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Вернитесь назад для того, чтобы увидеть все категории товаров ✅", reply_markup=inline.back_kb)


# Обработчик выбора товара
@dp.message_handler(lambda message: message.text.isdigit())
async def show_product_details(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, выбрал ли пользователь категорию
    if user_id not in user_category:
        await message.answer("Сначала выберите категорию в /catalog.")
        return
    
    product_index = int(message.text)-1
    category = user_category[user_id]   # Получаем категорию из словаря
    conn = await db.create_connection()
    cursor = await conn.cursor()

    # Получаем товары из категории
    products = await cursor.execute("SELECT product_id, name, description, price, photo FROM products WHERE category=?", (category,))
    products = await products.fetchall()
    await conn.close()

    if 0 <= product_index < len(products):
        # Отправляем карточку товара
        _, name, description, price, photo = products[product_index]
        await message.answer_photo(
            photo=open(photo, 'rb'),
            caption=f"📦 Название: {name}\n💬 Описание: {description}\n💰 Цена: {price} ₽"
        )

    else:
        await message.answer("Товар с таким номером не найден.")
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
# Обработчик команды /update
@dp.message_handler(commands=['update'])
async def send_update(message: types.Message):
    await message.answer("Пожалуйста, выберите действие.", reply_markup=reply.user_data_kb)


# Обработчик для обновления данных
@dp.message_handler(lambda message: message.text == "Обновить данные ♻")
async def update_data(message: types.Message):
    await message.answer("Давайте обновим ваши данные. Пожалуйста, введите email!", reply_markup=types.ReplyKeyboardRemove())
    await UserRegistration.waiting_for_email.set()


# Обработчик для удаления данных
@dp.message_handler(lambda message: message.text == 'Удалить данные ❌')
async def delete_data(message: types.Message):
    await message.answer("Вы действительно хотите удалить свои данные?", reply_markup=inline.delete_data_kb)

# Обработчик выбора действия
@dp.callback_query_handler(lambda call: call.data in ['yes', 'no'])
async def choice_delete(call: types.CallbackQuery):
    user_id = call.from_user.id

    if call.data == 'yes':
        await db.delete_user_data(user_id)
        await call.message.answer("✅ Все ваши данные удалены", reply_markup=types.ReplyKeyboardRemove())

    elif call.data == 'no':
        await call.message.answer("👍 Не волнуйтесь, ваши данные в порядке :)", reply_markup=types.ReplyKeyboardRemove())

    else:
        await call.message.answer("Выберите либо 'Да', либо 'Нет'")

    await call.answer()   # Подтверждение обработки callback-запроса


# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
# Обработчик для получения e-mail
@dp.message_handler(state=UserRegistration.waiting_for_email)
async def get_email(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    email = message.text

    if await db.check_user_exists(user_id):
        await db.update_user_data(user_id=user_id, email=email, phone=None)
        await UserRegistration.waiting_for_phone.set()
        await message.answer("Теперь введите ваш новый номер телефона.")

    else:
        # Сохраняем e-mail в базе данных
        await db.save_user_data(user_id=user_id, email=email, phone=None)
        await message.answer("Email добавлен")
        await message.answer("Теперь, пожалуйста, введите ваш номер телефона.")
        await UserRegistration.waiting_for_phone.set()


# Обработчик для получения телефона
@dp.message_handler(state=UserRegistration.waiting_for_phone)
async def get_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    phone = message.text

    if await db.check_user_exists(user_id) and phone==None:
        await db.update_user_data(user_id=user_id, email=None, phone=phone)
        await state.finish()
        await message.answer("Данные обновлены 👌")

    elif await db.check_user_exists(user_id):
        # Обновляем данные с номером телефона
        await db.save_user_data(user_id=user_id, email=None, phone=phone)
        await message.answer("Email и номер телефона добавленны")
        await message.answer("Регистрация завершена! Теперь вы можете просматривать товары. 🛍️")
        await state.finish()
# -------------------------------------------------------------------------------------------------------


'''======================================== ЗАПУСК БОТА ========================================'''
'''============================================================================================='''
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)