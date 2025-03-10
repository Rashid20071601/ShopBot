# Импорт библиотек
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from config import *
from keyboards import inline, reply
import config
from catalog.models import * # type: ignore
from asgiref.sync import sync_to_async


async def send_update(message: types.Message):
    await message.answer("Пожалуйста, выберите действие.", reply_markup=reply.user_data_kb)



async def delete_data(message: types.Message):
    await message.answer("Вы действительно хотите удалить свои данные?", reply_markup=inline.delete_data_kb)
    


async def choice_delete(call: types.CallbackQuery):
    user_id = call.from_user.id

    if call.data == 'yes':
        await sync_to_async(lambda: User.objects.get(user_id=user_id).delete())() # type: ignore
        await call.message.answer("✅ Все ваши данные удалены", reply_markup=types.ReplyKeyboardRemove())

    elif call.data == 'no':
        await call.message.answer("👍 Не волнуйтесь, ваши данные в порядке :)", reply_markup=types.ReplyKeyboardRemove())

    else:
        await call.message.answer("Выберите либо 'Да', либо 'Нет'")

    await call.answer()   # Подтверждение обработки callback-запроса



async def update_data(message: types.Message):
    await message.answer("Давайте обновим ваши данные. Пожалуйста, введите email!", reply_markup=types.ReplyKeyboardRemove())
    await UserRegistration.waiting_for_email.set()
    


async def get_email(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await sync_to_async(lambda: User.objects.filter(user_id=user_id).first())() # type: ignore
    try:
        email = message.text.strip() if message.text else None

        if user:
            await message.answer("Теперь, пожалуйста, введите ваш новый номер телефона для обновления данных.")

        else:
            await message.answer("Email добавлен")
            await message.answer("Теперь, пожалуйста, введите ваш номер телефона.")

        # Сохраняем e-mail в базе данных
        await UserRegistration.waiting_for_phone.set()
        await state.update_data(email=email)  # Сохраняем email в state
    
    except ValueError as e:
        await message.answer(f"Произошла ошибка: {str(e)}\nВведите команду /update заново.")



async def get_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await sync_to_async(lambda: User.objects.filter(user_id=user_id).first())() # type: ignore
    phone = message.text

    # Получаем сохранённый email из state
    user_data = await state.get_data()
    email = user_data.get('email')

    if not email:
        await message.answer("Произошла ошибка. Пожалуйста, начните заново, введя /start.")
        await state.finish()
        return

    # Проверяем, существует ли пользователь
    try:
        if user:
            await sync_to_async(lambda: User.objects.filter(user_id=user_id).update(email=email, phone=phone))() # type: ignore
            await message.answer("Данные обновлены 👌")

        else:
            await sync_to_async(lambda: User.objects.create(user_id=user_id, email=email, phone=phone))() # type: ignore
            await message.answer("Email и номер телефона добавлены")
            await message.answer("Регистрация завершена! Теперь вы можете просматривать товары. 🛍️")
    
    except ValueError as e:
        await message.answer(f"Произошла ошибка: {str(e)}\nВведите команду /update заново.")

    await state.reset_state(with_data=False)  




