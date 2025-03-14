# Импорт библиотек
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from keyboards import reply, inline
from config import *
from texts import texts
from catalog.models import * # type: ignore
from asgiref.sync import sync_to_async


async def send_welcome(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await sync_to_async(lambda: User.objects.filter(user_id=user_id).first())() # type: ignore
    if user:
        await send_start(message, state)
    else:
        await send_registration(message, state)


async def send_start(message: types.Message, state: FSMContext):
    await message.answer(texts.send_start, reply_markup=reply.start_kb)
    # Сохраняем состояние в FSM
    await state.update_data(current_step='start')


async def send_registration(message: types.Message, state: FSMContext):
    await message.answer(texts.send_registration)
    await UserRegistration.waiting_for_email.set()
    # Сохраняем состояние в FSM
    await state.update_data(current_step='start')



async def send_help(message: types.Message, state: FSMContext):
    await message.answer(texts.send_help, reply_markup=types.ReplyKeyboardRemove())
    await message.answer(texts.back, reply_markup=inline.back_kb)
    # Сохраняем состояние в FSM
    await state.update_data(current_step='help')


async def show_commands(message: types.Message, state: FSMContext):
    await message.answer(texts.show_commands, reply_markup=reply.commands_kb)
    await message.answer(texts.back, reply_markup=inline.back_kb)
    # Сохраняем состояние в FSM
    await state.update_data(current_step='commands')