from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_data_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Обновить данные ♻'), KeyboardButton(text='Удалить данные ❌')],
    ], resize_keyboard=True
)