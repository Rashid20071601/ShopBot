from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для удаления данных
delete_data_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅ Да, удалить', callback_data='yes'),
         InlineKeyboardButton(text='❌ Нет, оставить', callback_data='no')],
    ]
)

# Клавиатура для возврата
back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔙 Вернуться назад', callback_data='back')],
    ]
)

# Клавиатура для корзины
def cart_kb(product_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔙 Вернуться назад', callback_data='back')],
            [InlineKeyboardButton(text='🛒 Добавить в корзину', callback_data=f'cart_{product_id}')]
        ]
    )

# Клавиатура для очистки корзины
ask_clear_cart_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🧹 Да, очистить корзину', callback_data='confirm_clear_cart')],
        [InlineKeyboardButton(text='❌ Нет, оставить товары', callback_data='cancel_clear_cart')]
    ]
)