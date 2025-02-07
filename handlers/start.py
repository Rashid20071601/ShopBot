# Импорт библиотек
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from config import *
from database import db



async def send_welcome(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if await db.check_user_exists(user_id):
        await message.answer("Добро пожаловать в наш онлайн-магазин! 🛍️\nВведите /help для списка команд.")

    else:
        await message.answer("Добро пожаловать в наш онлайн-магазин! 🛍️\nМы начнем с регистрации. Введите ваш e-mail.")
        await UserRegistration.waiting_for_email.set()



async def send_help(message: types.Message):
    await message.answer("Доступные команды:"
                        "\n/start - Начать"
                        "\n/help - Помощь"
                        "\n/update - Обновить или удалить данные"
                        "\n/catalog - Посмотреть каталог товаров")