# Импорт библиотек
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from keyboards import inline, reply
from texts import texts
import logging
from catalog.models import * # type: ignore
from asgiref.sync import sync_to_async


'''============================================================================================================'''
async def show_categories(message: types.Message, state: FSMContext):
    """Отображает список категорий из БД"""
    
    try:
        categories = await sync_to_async(lambda: list(Category.objects.values_list('name', flat=True)))() # type: ignore

        # Сохраняем состояние в FSM
        await state.update_data(current_step='category', selected_category=None)

        # Проверяем, есть ли категории
        if not categories:
            await message.answer(texts.if_not_category)
            await message.answer(texts.back, reply_markup=inline.back_kb)
            return

        # Формируем кнопки с категориями
        category_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for category in categories:
            category_kb.add(category)  # Добавляем каждую категорию в кнопки

        await message.answer(texts.show_categories, reply_markup=category_kb)
        await message.answer(texts.back, reply_markup=inline.back_kb)
    
    except Exception as e:
        await message.answer(f"⚠ Произошла ошибка {e}. Пожалуйста, начните заново, введя /start. ♻")

'''============================================================================================================'''

'''============================================================================================================'''
async def show_products_by_category_wrapper(message: types.Message, state: FSMContext):
    """Обертка для вызова show_products_by_category только если введенный текст - это категория"""

    # Список всех категорий
    categories = await sync_to_async(lambda: list(Category.objects.values_list('name', flat=True)))()  # type: ignore

    if message.text in categories:
        await show_products_by_category(message, state)


async def show_products_by_category(message: types.Message, state: FSMContext, category=None):
    """Отображает товары выбранной категории"""

    try:
        # Если категория передана в аргументе (например, при возврате), используем её
        if category is None:
            category = message.text.strip() if message.text else None

        # Получаем данные состояния
        state_data = await state.get_data()
        selected_category = state_data.get('selected_category')

        # Если category не передано, берем из состояния
        if category is None:
            category = selected_category

        if not category:
            await message.answer(texts.if_category_empty)
            return
        
        # Сохраняем состояние в FSM
        await state.update_data(current_step='product', selected_category=category)

        # Проверяем, существует ли такая категория
        category_check = await sync_to_async(lambda: Category.objects.filter(name=category).first())() # type: ignore

        if not category_check:   # Если ничего не найдено, значит категории нет
            await message.answer(texts.if_not_category)
            return

        # Получаем товары из выбранной категории
        products = await sync_to_async(lambda: list(Product.objects.filter(category=category_check).values_list('product_id', 'name', 'price')))() # type: ignore

        if not products:
            await message.answer(texts.show_products_by_category_if_not_products, reply_markup=types.ReplyKeyboardRemove())
            await message.answer(texts.show_products_by_category_if_not_products_next, reply_markup=inline.back_kb)
        else:
            # Выводим товары в выбранной категории
            product_list = '\n'.join([f'➖➖➖➖➖\n🛍️ {i+1}. {product[1]}\n💵 Цена: {product[2]} ₽' for i, product in enumerate(products)])
            await message.answer(f"📂 Товары в категории '{category}': \n\n{product_list}\n\n\n🔍 Хотите узнать больше? Введите номер товара!", reply_markup=types.ReplyKeyboardRemove())
            await message.answer(texts.back, reply_markup=inline.back_kb)

    except Exception as e:
        await message.answer(f"⚠️ Упс! Что-то пошло не так при загрузке товаров: {e}. Пожалуйста, попробуйте ещё раз.")
    
'''============================================================================================================'''

'''============================================================================================================'''
async def show_product_details_wrapper(message: types.Message, state: FSMContext):
    # Получаем данные состояния
    state_data = await state.get_data()

    # Проверяем, на каком шаге находится пользователь
    current_step = state_data.get('current_step')

    if current_step == 'product':
        await show_product_details(message, state)


async def show_product_details(message: types.Message, state: FSMContext):
    """Отображает карточки выбраных товаров"""
    
    # Сохраняем состояние в FSM
    await state.update_data(current_step='product_details')

    # Получаем данные состояния
    state_data = await state.get_data()
    selected_category = state_data.get('selected_category')

    # Проверяем, выбрал ли пользователь категорию
    if selected_category is None:
        await message.answer(texts.if_category_empty)
        return
    
    product_index = int(message.text)-1
    category = await sync_to_async(lambda: Category.objects.get(name=selected_category))() # type: ignore

    # Получаем товары из категории
    products = await sync_to_async(lambda: list(Product.objects.filter(category=category).values_list('product_id', 'name', 'description', 'price', 'photo')))() # type: ignore

    if 0 <= product_index < len(products):
        # Отправляем карточку товара
        product_id, name, description, price, photo = products[product_index]
        photo_path = f"media/{photo}"
        await message.answer_photo(
            photo=open(photo_path, 'rb'),
            caption=f"🛍️ <b>Название:</b> {name}\n"
                    f"➖➖➖➖➖\n"
                    f"📝 <b>Описание:</b> {description}\n"
                    f"➖➖➖➖➖\n"
                    f"💰 <b>Цена:</b> {price} ₽\n"
                    f"➖➖➖➖➖\n"
                    f"🎯 <i>Добавьте товар в корзину, чтобы не потерять!</i>",
            reply_markup=inline.cart_kb(product_id),
            parse_mode="HTML"
        )

    else:
        await message.answer(texts.show_product_details_if_not_product, reply_markup=inline.back_kb)

    
    await state.reset_state(with_data=False)

