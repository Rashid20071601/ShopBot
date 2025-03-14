from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from texts import texts

user_data_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=texts.update_data), KeyboardButton(text=texts.delete_data)],
    ], resize_keyboard=True, one_time_keyboard=True
)

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=texts.cart), KeyboardButton(text=texts.catalog)],
        [KeyboardButton(text=texts.change_data)],
    ], resize_keyboard=True, one_time_keyboard=True
)

cart_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=texts.delete_product_from_cart), KeyboardButton(text=texts.clear_cart)],
    ], resize_keyboard=True, one_time_keyboard=True
)

commands_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=texts.update_data), KeyboardButton(text=texts.delete_data)],
        [KeyboardButton(text=texts.cart), KeyboardButton(text=texts.catalog)],
        [KeyboardButton(text=texts.delete_product_from_cart), KeyboardButton(text=texts.clear_cart)],
    ], resize_keyboard=True, one_time_keyboard=True
)