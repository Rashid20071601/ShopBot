# Импорт библиотек
from aiogram import types
from . import catalog
from aiogram.dispatcher.storage import FSMContext

async def back_button_handler(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные состояния
    state_data = await state.get_data()

    # Проверяем, на каком шаге находится пользователь
    current_step = state_data.get('current_step')
    selected_category = state_data.get('selected_category')

    if not current_step:   # Если не удалось получить шаг (что-то пошло не так)
        await call.message.answer("Не удалось вернуться к предыдущему шагу.")
        return

    # Возвращаем пользователя на предыдущий этап
    if current_step == 'product_details':
        await state.update_data(current_step='product')  # Назад к списку товаров
        if selected_category:
            await catalog.show_products_by_category(message=call.message, category=selected_category, state=state)  # Возвращаем к товарам в категории
        else:
            await call.message.answer("Сначала выберите категорию.")
    
    elif current_step == 'product':
        await state.update_data(current_step='category')  # Назад к категориям
        await catalog.show_categories(call.message, state=state)  # Возвращаем к списку категорий

    elif current_step == 'category':
        await call.message.answer("Вы уже на начальном шаге каталога.")
    
    else:
        await call.message.answer("Не удалось вернуться к предыдущему шагу.")
    
    await call.answer()