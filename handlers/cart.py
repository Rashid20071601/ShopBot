# Импорт библиотек
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from keyboards import inline, reply
from texts import texts
from config import CartState
from catalog.models import * # type: ignore
from asgiref.sync import sync_to_async


# Функция просмотра корзины
async def view_cart(message: types.Message, state: FSMContext):
    user_id = message.from_user.id  # Получаем ID пользователя
    user = await sync_to_async(lambda: User.objects.get(pk=user_id))() # type: ignore

    # Сохраняем состояние в FSM
    # state.update_data(current_step='cart')

    # Получаем товары в корзине с их названиями и ценами
    cart_items = await sync_to_async(lambda: list(Cart.objects.filter(user=user).select_related('product').values('product__name', 'product__price', 'quantity')))() # type: ignore
    
    if not cart_items:
        await message.answer(texts.view_cart_if_empty, reply_markup=types.ReplyKeyboardRemove())
    else:
        cart_items_str = '\n'.join([f"{i+1}. {item['product__name']} - {item['product__price']} руб. - {item['quantity']} шт." for i, item in enumerate(cart_items)])
        # Возвращаем товары в корзине пользователя
        await message.answer(f"{texts.view_cart}\n\n{cart_items_str}", reply_markup=reply.cart_kb)


# Функция добавления товара в корзину
async def add_to_cart(call: types.CallbackQuery):

    user_id = call.from_user.id
    product_id = int(call.data.split('_')[-1])  # Извлекаем ID товара из callback-данных

    user = await sync_to_async(lambda: User.objects.get(pk=user_id))() # type: ignore
    product = await sync_to_async(lambda: Product.objects.get(pk=product_id))() # type: ignore

    # Проверяем, существует ли товар в таблице products
    if not await sync_to_async(lambda: Product.objects.filter(product_id=product_id).exists())(): # type: ignore
        await call.message.answer(texts.add_to_cart_if_not_product, reply_markup=types.ReplyKeyboardRemove())
        return

    # Проверяем, есть ли уже этот товар в корзине пользователя
    cart_item, created = await sync_to_async(lambda: Cart.objects.get_or_create(user=user, product=product))() # type: ignore

    if not created:
        # Если товар уже в корзине, обновляем его количество
        cart_item.quantity += 1

    # Сохраняем корзину
    await sync_to_async(cart_item.save)()
    
    await call.message.answer(texts.add_to_cart)
    await call.answer()


# Функции удаления товара
async def start_remove_from_cart(message: types.Message, state: FSMContext):
    await message.answer(texts.start_remove_from_cart, reply_markup=types.ReplyKeyboardRemove())
    # Устанавливаем состояние ожидания номера товара
    await CartState.waiting_for_product_id.set()

async def process_remove_from_cart(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    user = await sync_to_async(lambda: User.objects.get(pk=user_id))() # type: ignore

    # Проверяем, что пользователь ввел число
    if not message.text.isdigit():
        await message.answer(texts.process_remove_from_cart_if_undefined)

    product_id = int(message.text)-1

    # Получаем товары в корзине
    cart_items = await sync_to_async(lambda: list(Cart.objects.filter(user=user).select_related('product').values_list('product__product_id', 'quantity')))() # type: ignore

    if 0 <= product_id < len(cart_items):
        product_to_delete, quantity = cart_items[product_id]
        if quantity > 1:
            # Если товаров больше одного, уменьшаем количество
            await sync_to_async(lambda: Cart.objects.filter(user=user, product_id=product_to_delete).update(quantity=quantity - 1))()  # type: ignore
        else:
            # Если товар один, удаляем его из корзины
            await sync_to_async(lambda: Cart.objects.filter(user=user, product_id=product_to_delete).delete())()  # type: ignore
        await message.answer(texts.process_remove_from_cart)
        await view_cart(message, state)

    else:
        await message.answer(texts.process_remove_from_cart_if_not_product)
        await view_cart(message, state)

    # Завершаем состояние
    await state.finish()



async def ask_clear_cart(message: types.Message):
    await message.answer(texts.ask_clear_cart, reply_markup=inline.ask_clear_cart_kb)


async def do_not_clear_cart(call: types.CallbackQuery):
    await call.message.answer(texts.do_not_clear_cart)
    await call.answer()


# Функция очистки корзины
async def clear_cart(call: types.CallbackQuery):
    user_id = call.from_user.id
    
    await sync_to_async(lambda: Cart.objects.filter(user_id=user_id).delete())() # type: ignore

    await call.message.answer(texts.clear_cart)
    await call.answer()
