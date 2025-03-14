# Импорт библиотек
import logging
from aiogram import types
from . import catalog, start
from texts import texts
from aiogram.dispatcher.storage import FSMContext

async def back_button_handler(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные состояния
    state_data = await state.get_data()

    # Проверяем, на каком шаге находится пользователь
    current_step = state_data.get('current_step')
    selected_category = state_data.get('selected_category')

    if not current_step:   # Если не удалось получить шаг (что-то пошло не так)
        await call.message.answer(texts.back_error)
        return
    

# ========================= START ========================= #
    # Если пользователь на начальном этапе, просто отменяем команду
    if current_step == 'start':
        await call.message.answer(texts.back_if_start)

    elif current_step == 'help' or current_step == 'commands':
        await state.update_data(current_step='start')
        await start.send_start(call.message, state)


# ========================= CATALOG ========================= #
    # Возвращаем пользователя на предыдущий этап
    elif current_step == 'product_details':
        await state.update_data(current_step='product')  # Назад к списку товаров
        await catalog.show_products_by_category(call.message, state, category=selected_category)
    
    elif current_step == 'product':
        await state.update_data(current_step='category')  # Назад к категориям
        await catalog.show_categories(call.message, state=state)  # Возвращаем к списку категорий

    elif current_step == 'category':
        await state.update_data(current_step='start')
        await start.send_start(call.message, state)
    

# ========================= ERROR ========================= #
    else:
        await call.message.answer(texts.back_error)
    
    await call.answer()