from gc import callbacks

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text='Магазин', callback_data=''),
         InlineKeyboardButton(text='VPN', callback_data='')],

        [InlineKeyboardButton(text='Профиль', callback_data='')],

        [InlineKeyboardButton(text='Правила', callback_data=''),
         InlineKeyboardButton(text='Помощь', callback_data=''),
         InlineKeyboardButton(text='Сотрудничество', callback_data='')],

        [InlineKeyboardButton(text='', callback_data='')],
    ]
)