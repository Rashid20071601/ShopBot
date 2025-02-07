# Импорт библиотек
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from config import *
from keyboards import inline, reply
from database import db



async def send_update(message: types.Message):
    await message.answer("Пожалуйста, выберите действие.", reply_markup=reply.user_data_kb)



async def delete_data(message: types.Message):
    await message.answer("Вы действительно хотите удалить свои данные?", reply_markup=inline.delete_data_kb)
    


async def choice_delete(call: types.CallbackQuery):
    user_id = call.from_user.id

    if call.data == 'yes':
        await db.delete_user_data(user_id)
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
    email = message.text.strip() if message.text else None

    if await db.check_user_exists(user_id):
        await state.update_data(email=email)  # Сохраняем email в state
        await UserRegistration.waiting_for_phone.set()
        await message.answer("Теперь введите ваш новый номер телефона.")

    else:
        # Сохраняем e-mail в базе данных
        await state.update_data(email=email)  # Сохраняем email в state
        await message.answer("Email добавлен")
        await message.answer("Теперь, пожалуйста, введите ваш номер телефона.")
        await UserRegistration.waiting_for_phone.set()



async def get_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    phone = message.text

    # Получаем сохранённый email из state
    user_data = await state.get_data()
    email = user_data.get('email')

    if not email:
        await message.answer("Произошла ошибка. Пожалуйста, начните заново, введя /start.")
        await state.finish()
        return

    # Проверяем, существует ли пользователь
    if await db.check_user_exists(user_id):
        await db.update_user_data(user_id=user_id, email=email, phone=phone)
        await message.answer("Данные обновлены 👌")

    else:
        await db.save_user_data(user_id=user_id, email=email, phone=phone)
        await message.answer("Email и номер телефона добавлены")
        await message.answer("Регистрация завершена! Теперь вы можете просматривать товары. 🛍️")

    await state.finish()



