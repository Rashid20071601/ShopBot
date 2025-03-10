# Импорт библиотек
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from keyboards import reply, inline
from config import *
import config
from catalog.models import * # type: ignore
from asgiref.sync import sync_to_async



async def send_welcome(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await sync_to_async(lambda: User.objects.filter(user_id=user_id).first())() # type: ignore

    if user:
        await message.answer("Добро пожаловать в наш онлайн-магазин! 🛍️\nНажмит на кнопку ниже\nИли введите /help для списка команд.",
                             reply_markup=reply.start_kb)
        # Сохраняем состояние в FSM
        # state.update_data(current_step='start')

    else:
        await message.answer("Добро пожаловать в наш онлайн-магазин! 🛍️\nМы начнем с регистрации. Введите ваш e-mail.")
        await UserRegistration.waiting_for_email.set()



async def send_help(message: types.Message, state: FSMContext):
    await message.answer("Доступные команды:"
                        "\n/start - Начать"
                        "\n/help - Помощь"
                        "\n/update - Обновить или удалить данные"
                        "\n/catalog - Посмотреть каталог товаров")
    # Сохраняем состояние в FSM
    # state.update_data(current_step='help')