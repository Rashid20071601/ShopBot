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

def cart_kb(product_id: int):
    return InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад  🔙', callback_data='back')],
        [InlineKeyboardButton(text='Добавить в корзину', callback_data=f'cart_{product_id}')]
    ]
)

ask_clear_cart_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Да, очистить", callback_data="confirm_clear_cart")],
        [InlineKeyboardButton("Нет, оставить", callback_data="cancel_clear_cart")]
    ]
)