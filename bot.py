# Импорт библиотек
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import sys
import config
from texts import texts
import handlers.back
import handlers.cart
import handlers.catalog
import handlers.data
import handlers.start


# Настройка логирования
# logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Создаем обработчик для вывода логов в консоль
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Добавляем обработчик в логгер
logger = logging.getLogger()
logger.addHandler(console_handler)


# --------------- Инициализация бота и диспетчера --------------- #
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

EXCLUDED_BUTTONS = [
    texts.cart,
    texts.delete_product_from_cart,
    texts.clear_cart,
    texts.catalog,
    texts.update_data,
    texts.delete_data,
    texts.change_data,
    ]


'''=============================== ОБРАБОТЧИК КОМАНД ==============================================='''

# Обработчик команды /start
logger.info("Обработчик команды /start зарегистрирован")
dp.message_handler(commands=['start'])(handlers.start.send_welcome)

# Обработчик команды /help
logger.info("Обработчик команды /help зарегистрирован")
dp.message_handler(commands=['help'])(handlers.start.send_help)

# Обработчик команды /catalog для отображения категорий
dp.message_handler(commands=['catalog'])(handlers.catalog.show_categories)

# Обработчик выбора категории
logger.info("Обработчик выбора категории зарегистрирован")
dp.message_handler(lambda message: message.text and not message.text.isdigit() and message.text not in EXCLUDED_BUTTONS)(handlers.catalog.show_products_by_category_wrapper)

# Обработчик выбора товара
logger.info("Обработчик выбора товара зарегистрирован")
dp.message_handler(lambda message: message.text.isdigit())(handlers.catalog.show_product_details_wrapper)

# Обработчик нажатия кнопки "Назад"
logger.info("Обработчик кнопки 'Назад' зарегистрирован")
dp.callback_query_handler(lambda call: call.data == 'back')(handlers.back.back_button_handler)

# Обработчик команды /update
dp.message_handler(commands=['update'])(handlers.data.send_update)

# Обработчик для обновления данных
dp.message_handler(lambda message: message.text == "Обновить данные ♻")(handlers.data.update_data)

# Обработчик для удаления данных
dp.message_handler(lambda message: message.text == 'Удалить данные ❌')(handlers.data.delete_data)

# Обработчик выбора действия (подтверждение удаления)
logger.info("Обработчик выбора действия (подтверждение удаления) зарегистрирован")
dp.callback_query_handler(lambda call: call.data in ['yes', 'no'])(handlers.data.choice_delete)

# Обработчик для получения e-mail
logger.info("Обработчик получения e-mail зарегистрирован")
dp.message_handler(state=config.UserRegistration.waiting_for_email)(handlers.data.get_email)

# Обработчик для получения телефона
logger.info("Обработчик получения телефона зарегистрирован")
dp.message_handler(state=config.UserRegistration.waiting_for_phone)(handlers.data.get_phone)

# Обработчик просмотра товаров в корзине
dp.message_handler(lambda message: message.text == 'Корзина')(handlers.cart.view_cart)

# Обработчик для добавления товара в корзину
logger.info("Обработчик добавления товара в корзину зарегистрирован")
dp.callback_query_handler(lambda call: call.data.startswith('cart_'))(handlers.cart.add_to_cart)

# Обработчик удаления товаров в корзине
dp.message_handler(lambda message: message.text == 'Удалить товар')(handlers.cart.start_remove_from_cart)
dp.message_handler(state=config.CartState.waiting_for_product_id)(handlers.cart.process_remove_from_cart)

# Обработчик очистки корзины
dp.message_handler(lambda message: message.text == 'Очистить корзину')(handlers.cart.ask_clear_cart)
dp.callback_query_handler(lambda call: call.data == 'confirm_clear_cart')(handlers.cart.clear_cart)
dp.callback_query_handler(lambda call: call.data == 'cancel_clear_cart')(handlers.cart.do_not_clear_cart)


'''======================================== ЗАПУСК БОТА ========================================'''

logger.info("Запуск бота...")
if __name__ == '__main__':
    executor.start_polling(dp)