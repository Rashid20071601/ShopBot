from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

delete_data_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text='Да', callback_data='yes'),
        InlineKeyboardButton(text='Нет', callback_data='no')],
    ]
)

back_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text='Назад  🔙', callback_data='back')],
    ]
)