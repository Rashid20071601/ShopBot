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


async def on_startup(dp):
    """Подключение к базе данных при старте бота"""
    await db.create_user_table()


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
    await message.answer("Доступные команды:\n/start - Начать\n/help - Помощь\n/update - Обновить или удалить данные")

# Обработчик команды /update
@dp.message_handler(commands=['update'])
async def send_update(message: types.Message):
    await message.answer("Пожалуйста, выберите действие.", reply_markup=reply.user_data_kb)

# Обработчик для обновления данных
@dp.message_handler(lambda message: message.text == "Обновить данные ♻")
async def update_data(message: types.Message):
    await message.answer("Давайте обновим ваши данные. Пожалуйста, введите email!")
    await UserRegistration.waiting_for_email.set()

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
        print(2)
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
    if await db.check_user_exists(user_id):
        await db.update_user_data(user_id=user_id, email=None, phone=phone)
        await state.finish()
        await message.answer("Данные обновлены 👌")
    else:
        # Обновляем данные с номером телефона
        await db.save_user_data(user_id=user_id, email=None, phone=phone)
        await message.answer("Email и номер телефона добавленны")
        await message.answer("Регистрация завершена! Теперь вы можете просматривать товары. 🛍️")
        await state.finish()


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)