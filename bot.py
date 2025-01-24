# Импорт библиотек
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from utils import misc
from config import BOT_TOKEN
from keyboards import inline, reply

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Добро пожаловать в наш онлайн-магазин! 🛍️\nВведите /help для списка команд.")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer("Доступные команды:\n/start - Начать\n/help - Помощь")


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)