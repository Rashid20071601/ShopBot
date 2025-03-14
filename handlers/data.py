# Импорт библиотек
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from config import *
from keyboards import inline, reply
from texts import texts
import config
from catalog.models import * # type: ignore
from asgiref.sync import sync_to_async


async def send_update(message: types.Message):
    await message.answer(texts.send_update, reply_markup=reply.user_data_kb)



async def delete_data(message: types.Message):
    await message.answer(texts.delete_data_process, reply_markup=inline.delete_data_kb)
    


async def choice_delete(call: types.CallbackQuery):
    user_id = call.from_user.id

    if call.data == 'yes':
        await sync_to_async(lambda: User.objects.get(user_id=user_id).delete())() # type: ignore
        await call.message.answer(texts.choice_delete_yes, reply_markup=types.ReplyKeyboardRemove())

    elif call.data == 'no':
        await call.message.answer(texts.choice_delete_no, reply_markup=types.ReplyKeyboardRemove())

    else:
        await call.message.answer(texts.choice_delete_else)

    await call.answer()   # Подтверждение обработки callback-запроса



async def update_data(message: types.Message):
    await message.answer(texts.update_data_process, reply_markup=types.ReplyKeyboardRemove())
    await UserRegistration.waiting_for_email.set()
    


async def get_email(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await sync_to_async(lambda: User.objects.filter(user_id=user_id).first())() # type: ignore
    try:
        email = message.text.strip() if message.text else None

        if user:
            await message.answer(texts.get_email_if_user)

        else:
            await message.answer(texts.get_email_else)
            await message.answer(texts.get_email_else_next)

        # Сохраняем e-mail в базе данных
        await UserRegistration.waiting_for_phone.set()
        await state.update_data(email=email)  # Сохраняем email в state
    
    except ValueError as e:
        await message.answer(f"Произошла ошибка: {str(e)}\nВведите команду /start заново.")



async def get_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await sync_to_async(lambda: User.objects.filter(user_id=user_id).first())() # type: ignore
    phone = message.text

    # Получаем сохранённый email из state
    user_data = await state.get_data()
    email = user_data.get('email')

    if not email:
        await message.answer(texts.get_phone_if_not_email)
        await state.finish()
        return

    # Проверяем, существует ли пользователь
    try:
        if user:
            await sync_to_async(lambda: User.objects.filter(user_id=user_id).update(email=email, phone=phone))() # type: ignore
            await message.answer(texts.get_phone_if_user)

        else:
            await sync_to_async(lambda: User.objects.create(user_id=user_id, email=email, phone=phone))() # type: ignore
            await message.answer(texts.get_phone_else)
            await message.answer(texts.get_phone_else_next)
    
    except ValueError as e:
        await message.answer(f"Произошла ошибка: {str(e)}\nВведите команду /start заново.")

    await state.reset_state(with_data=False)  




