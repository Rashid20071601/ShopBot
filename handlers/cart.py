# Импорт библиотек
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from keyboards import inline, reply
from database import db
from config import CartState
import config
from catalog.models import * # type: ignore
from asgiref.sync import sync_to_async


# Функция просмотра корзины
async def view_cart(message: types.Message, state: FSMContext):
    user_id = message.from_user.id  # Получаем ID пользователя
    user = await sync_to_async(User.objects.get(pk=user_id)) # type: ignore

    # Сохраняем состояние в FSM
    # state.update_data(current_step='cart')

    # Получаем товары в корзине с их названиями и ценами
    cart_items = await sync_to_async(Cart.objects.filter(user=user).select_related('product').values('product__name', 'product__price', 'quantity')) # type: ignore
    
    if not cart_items:
        await message.answer("Ваша корзина пуста.")
    else:
        cart_items = '\n'.join([f"{i+1}. {item[0]} - {item[1]} руб. - {item[2]} шт." for i, item in enumerate(cart_items)])
        # Возвращаем товары в корзине пользователя
        await message.answer(f"Ваша корзина\n\n{cart_items}", reply_markup=reply.cart_kb)


# Функция добавления товара в корзину
async def add_to_cart(call: types.CallbackQuery):

    user_id = call.from_user.id
    product_id = int(call.data.split('_')[-1])  # Извлекаем ID товара из callback-данных

    user = await sync_to_async(lambda: User.objects.get(pk=user_id))() # type: ignore
    product = await sync_to_async(lambda: Product.objects.get(pk=product_id))() # type: ignore

    # Проверяем, существует ли товар в таблице products
    if not Product.objects.filter(product_id=product_id).exists(): # type: ignore
        await call.message.answer("Ошибка: товар не существует!")
        return

    # Проверяем, есть ли уже этот товар в корзине пользователя
    cart_item, created = await sync_to_async(lambda: Cart.objects.get_or_create(user=user, product=product))() # type: ignore

    if not created:
        # Если товар уже в корзине, обновляем его количество
        await cart_item.quantity + 1

    await cart_item.save()
    
    await call.message.answer("Товар добавлен в корзину!")
    await call.answer()


# Функции удаления товара
async def start_remove_from_cart(message: types.Message, state: FSMContext):
    await message.answer("Выберите номер товара, который хотите удалить!")
    # Устанавливаем состояние ожидания номера товара
    await CartState.waiting_for_product_id.set()

async def process_remove_from_cart(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    user = await sync_to_async(User.objects.get(pk=user_id)) # type: ignore

    # Проверяем, что пользователь ввел число
    if not message.text.isdigit():
        await message.answer("Введите коррекный номер товара (число).")

    product_id = int(message.text)-1

    # Получаем товары в корзине
    cart_items = await sync_to_async(lambda: list(Cart.objects.filter(user=user).select_related('product').values_list('product__id', flat=True))) # type: ignore

    if 0 <= product_id < len(cart_items):
        product_to_delete = cart_items[product_id]
        # Удаляем товар из корзины через ORM
        await sync_to_async(lambda: Cart.objects.filter(user=user, product_id=product_to_delete).delete)() # type: ignore
        await message.answer("Товар удалён из корзины!")

    else:
        await message.answer("Такого товара нет в корзине!")

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
    
    await sync_to_async(lambda: Cart.objects.filter(user_id=user_id).delete)() # type: ignore

    await call.message.answer("Корзина очищена.")
    await call.answer()
