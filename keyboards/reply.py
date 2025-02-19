from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_data_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Обновить данные ♻'), KeyboardButton(text='Удалить данные ❌')],
    ], resize_keyboard=True
)

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Корзина')]
    ], resize_keyboard=True, one_time_keyboard=True
)

cart_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Удалить товар')],
        [KeyboardButton(text='Очистить корзину')]
    ], resize_keyboard=True, one_time_keyboard=True
)