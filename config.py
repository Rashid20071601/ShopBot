# Импорт библиотек
from aiogram.dispatcher.filters.state import State, StatesGroup

BOT_TOKEN = "7715508815:AAFPH4WcTbEyJym-WB_DeyaROVpVlUd5oWk"

# Определяем состояния
class UserRegistration(StatesGroup):
    waiting_for_email = State()
    waiting_for_phone = State()

class CartState(StatesGroup):
    waiting_for_product_id = State()