# Импорт библиотек
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
import logging
from config import *
import handlers.back
import handlers.cart
import handlers.catalog
import handlers.data
import handlers.start
from keyboards import inline, reply
from database import db
import handlers


# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
EXCLUDED_BUTTONS = [
    "Корзина",
    "Удалить товар",
    "Очистить корзину",
    ]


async def on_startup(dp):
    """Подключение к базе данных при старте бота"""
    await db.create_user_table()
    await db.create_product_table()
    await db.create_cart_table()


'''=============================== ОБРАБОТЧИК КОМАНД ==============================================='''
'''================================================================================================='''


# Обработчик команды /start
dp.message_handler(commands=['start'])(handlers.start.send_welcome)

# Обработчик команды /help
dp.message_handler(commands=['help'])(handlers.start.send_help)

# Обработчик команды /catalog для отображения категорий
dp.message_handler(commands=['catalog'])(handlers.catalog.show_categories)

# Обработчик выбора категории
dp.message_handler(lambda message: message.text and not message.text.isdigit() and message.text not in EXCLUDED_BUTTONS)(handlers.catalog.show_products_by_category)

# Обработчик выбора товара
dp.message_handler(lambda message: message.text.isdigit())((handlers.catalog.show_product_details))

# Обработчик нажатия кнопки "Назад"
dp.callback_query_handler(lambda call: call.data == 'back')(handlers.back.back_button_handler)

# Обработчик команды /update
dp.message_handler(commands=['update'])(handlers.data.send_update)

# Обработчик для обновления данных
dp.message_handler(lambda message: message.text == "Обновить данные ♻")(handlers.data.update_data)

# Обработчик для удаления данных
dp.message_handler(lambda message: message.text == 'Удалить данные ❌')(handlers.data.delete_data)

# Обработчик выбора действия
dp.callback_query_handler(lambda call: call.data in ['yes', 'no'])(handlers.data.choice_delete)

# Обработчик для получения e-mail
dp.message_handler(state=UserRegistration.waiting_for_email)(handlers.data.get_email)

# Обработчик для получения телефона
dp.message_handler(state=UserRegistration.waiting_for_phone)(handlers.data.get_phone)

# Обработчик просмотра товаров в корзине
dp.message_handler(lambda message: message.text == 'Корзина')(handlers.cart.view_cart)

# Обрботчик для добавления товара в корзину
dp.callback_query_handler(lambda call: call.data.startswith('cart_'))(handlers.cart.add_to_cart)

# Обработчик удаления товаров в корзине
dp.message_handler(lambda message: message.text == 'Удалить товар')(handlers.cart.start_remove_from_cart)
dp.message_handler(state=CartState.waiting_for_product_id)(handlers.cart.process_remove_from_cart)

# Обработчик очистки корзины
dp.message_handler(lambda message: message.text == 'Очистить корзину')(handlers.cart.ask_clear_cart)
dp.callback_query_handler(lambda call: call.data == 'confirm_clear_cart')(handlers.cart.clear_cart)
dp.callback_query_handler(lambda call: call.data == 'cancel_clear_cart')(handlers.cart.do_not_clear_cart)


# ======================================== ЗАПУСК БОТА ========================================
# =============================================================================================

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)