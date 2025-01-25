# Импорт библиотек
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import asyncio
from utils import misc
from config import BOT_TOKEN
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
async def send_welcome(message: types.Message):
    await message.answer("Добро пожаловать в наш онлайн-магазин! 🛍️\nВведите /help для списка команд.")

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer("Доступные команды:\n/start - Начать\n/help - Помощь")


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)