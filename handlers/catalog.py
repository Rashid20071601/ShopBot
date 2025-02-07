# Импорт библиотек
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from keyboards import inline, reply
from database import db



'''============================================================================================================'''
async def show_categories(message: types.Message, state: FSMContext):
    """Отображает список категорий из БД"""

    # Создаем соединение с базой данных
    conn = await db.create_connection()
    cursor = await conn.cursor()

    # Получаем уникальные категории
    categories = await cursor.execute("SELECT DISTINCT category FROM products")
    categories = await categories.fetchall()

    await conn.close()

    # Сохраняем состояние в FSM
    await state.update_data(current_step='category', selected_category=None)

    # Проверяем, есть ли категории
    if not categories:
        await message.answer("Категорий пока нет.")
        return

    # Формируем кнопки с категориями
    category_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        category_kb.add(category[0])  # Добавляем каждую категорию в кнопки

    await message.answer("Выберите категорию", reply_markup=category_kb)
'''============================================================================================================'''

'''============================================================================================================'''
async def show_products_by_category(message: types.Message, state: FSMContext, category=None):
    """Отображает товары выбранной категории"""
    category = message.text

    # Получаем данные состояния
    state_data = await state.get_data()
    selected_category = state_data.get('selected_category')

    # Если category не передано, берем из сообщения
    if selected_category is None:
        selected_category = message.text.strip() if message.text else None

    if not selected_category:
        await message.answer("Ошибка: категория не определена. Пожалуйста, выберите категорию.")
        return
    
    # Сохраняем состояние в FSM
    await state.update_data(current_step='product', selected_category=selected_category)

    conn = await db.create_connection()
    cursor = await conn.cursor()

    # Проверяем, существует ли такая категория
    category_check = await cursor.execute("SELECT DISTINCT category FROM products WHERE category=?", (selected_category,))
    category_check = await category_check.fetchone()  # Получаем одну строку

    if not category_check:   # Если ничего не найдено, значит категории нет
        await message.answer("Такой категории нет, выберите из списка.")
        await conn.close()
        return

    # Получаем товары из выбранной категории
    products = await cursor.execute("SELECT product_id, name, price FROM products WHERE category=?", (selected_category,))
    products = await products.fetchall()
    await conn.close()

    if not products:
        await message.answer("В этой категории пока нет товаров.", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Вернитесь назад для того, чтобы увидеть все категории товаров ✅", reply_markup=inline.back_kb)
    else:
        # Выводим товары в выбранной категории
        product_list = '\n'.join([f'{i+1}. {product[1]} - {product[2]} ₽' for i, product in enumerate(products)])
        await message.answer(f"Товары в категории '{category}': \n\n{product_list}", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Введите номер товара для подробностей.", reply_markup=inline.back_kb)
'''============================================================================================================'''

'''============================================================================================================'''
async def show_product_details(message: types.Message, state: FSMContext):
    """Отображает карточки выбраных товаров"""

    # Сохраняем состояние в FSM
    await state.update_data(current_step='product_details')

    # Получаем данные состояния
    state_data = await state.get_data()
    selected_category = state_data.get('selected_category')

    # Проверяем, выбрал ли пользователь категорию
    if selected_category is None:
        await message.answer("Сначала выберите категорию в /catalog.")
        return
    
    product_index = int(message.text)-1
    category = selected_category
    conn = await db.create_connection()
    cursor = await conn.cursor()

    # Получаем товары из категории
    products = await cursor.execute("SELECT product_id, name, description, price, photo FROM products WHERE category=?", (category,))
    products = await products.fetchall()
    await conn.close()

    if 0 <= product_index < len(products):
        # Отправляем карточку товара
        _, name, description, price, photo = products[product_index]
        await message.answer_photo(
            photo=open(photo, 'rb'),
            caption=f"📦 Название: {name}\n💬 Описание: {description}\n💰 Цена: {price} ₽",
            reply_markup=inline.back_kb
        )

    else:
        await message.answer("Товар с таким номером не найден.")