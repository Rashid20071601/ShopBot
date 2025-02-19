# Импорт библиотек
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from keyboards import inline, reply
from database import db
from config import CartState


# Функция просмотра корзины
async def view_cart(message: types.Message, state: FSMContext):
    user_id = message.from_user.id  # Получаем ID пользователя
    
    conn = await db.create_connection()
    cursor = await conn.cursor()

    # Сохраняем состояние в FSM
    # state.update_data(current_step='cart')

    cart = await cursor.execute("SELECT * FROM cart")
    cart = await cart.fetchall()
    print(cart)

    # Получаем товары в корзине с их названиями и ценами
    cart_items = await cursor.execute('''
                                    SELECT p.name, p.price, c.quantity 
                                    FROM cart c
                                    JOIN products p ON c.product_id = p.product_id
                                    WHERE c.user_id = ?
                                    ''',
                                    (user_id,))
    cart_items = await cart_items.fetchall()
    
    if not cart_items:
        await message.answer("Ваша корзина пуста.")
    else:
        cart_items = '\n'.join([f"{i+1}. {item[0]} - {item[1]} руб. - {item[2]} шт." for i, item in enumerate(cart_items)])
        # Возвращаем товары в корзине пользователя
        await message.answer(f"Ваша корзина\n\n{cart_items}", reply_markup=reply.cart_kb)

    await conn.close()


# Функция добавления товара в корзину
async def add_to_cart(call: types.CallbackQuery):
    conn = await db.create_connection()
    cursor = await conn.cursor()

    user_id = call.from_user.id
    product_id = int(call.data.split('_')[-1])  # Извлекаем ID товара из callback-данных
    quantity = 1  # По умолчанию добавляем 1 шт. в корзину

    # Проверяем, существует ли товар в таблице products
    product_exists = await cursor.execute("SELECT 1 FROM products WHERE product_id = ?", (product_id,))
    if not await product_exists.fetchone():
        await call.message.answer("Ошибка: товар не существует!")
        await conn.close()
        return

    # Проверяем, есть ли уже этот товар в корзине пользователя
    existing_item = await cursor.execute("SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    existing_item = await existing_item.fetchone()

    if existing_item:
        # Если товар уже в корзине, обновляем его количество
        new_quantity = existing_item[0] + 1
        await cursor.execute("UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?", (new_quantity, user_id, product_id))
    
    else:
        # Если товара нет в корзине, добавляем его
        await cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)", (user_id, product_id, quantity))

    await call.message.answer("Товар добавлен в корзину!")

    await conn.commit()
    await conn.close()
    await call.answer()


# Функции удаления товара
async def start_remove_from_cart(message: types.Message, state: FSMContext):
    await message.answer("Выберите номер товара, который хотите удалить!")
    # Устанавливаем состояние ожидания номера товара
    await CartState.waiting_for_product_id.set()

async def process_remove_from_cart(message: types.Message, state: FSMContext):
    conn = await db.create_connection()
    cursor = await conn.cursor()
    
    user_id = message.from_user.id

    # Проверяем, что пользователь ввел число
    if not message.text.isdigit():
        await message.answer("Введите коррекный номер товара (число).")

    product_id = int(message.text)-1

    # Получаем товары в корзине
    cart_items = await cursor.execute("SELECT product_id FROM cart WHERE user_id = ?", (user_id,))
    cart_items = await cart_items.fetchall()

    if 0 <= product_id < len(cart_items):
        product_to_delete = cart_items[product_id][0]
        await cursor.execute("DELETE FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_to_delete))
        await conn.commit()
        await message.answer("Товар удалён из корзины!")

    else:
        await message.answer("Такого товара нет в корзине!")

    await conn.close()

    # Завершаем состояние
    await state.finish()



async def ask_clear_cart(message: types.Message):
    await message.answer("Вы действительно хотите очистить корзину?", reply_markup=inline.ask_clear_cart_kb)


async def do_not_clear_cart(call: types.CallbackQuery):
    await call.message.answer("Очистка корзины отменена! Вы можете продолжить покупки.")
    await call.answer()


# Функция очистки корзины
async def clear_cart(call: types.CallbackQuery):
    user_id = call.from_user.id

    conn = await db.create_connection()
    cursor = await conn.cursor()
    
    await cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))

    await conn.commit()
    await conn.close()

    await call.message.answer("Корзина очищена.")
    await call.answer()
