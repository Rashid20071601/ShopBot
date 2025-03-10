# Импорт библиотек
from aiogram.dispatcher.filters.state import State, StatesGroup

BOT_TOKEN = "7715508815:AAFPH4WcTbEyJym-WB_DeyaROVpVlUd5oWk"

# Определяем состояния
class UserRegistration(StatesGroup):
    waiting_for_email = State()
    waiting_for_phone = State()

class CartState(StatesGroup):
    waiting_for_product_id = State()


import os
import sys
import django

# Получаем путь к корневой директории проекта (ShopBot)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)  # Добавляем корневую директорию проекта

# Добавляем `admin_panel` в sys.path
ADMIN_PANEL_DIR = os.path.join(BASE_DIR, "admin_panel")
sys.path.append(ADMIN_PANEL_DIR)

# Устанавливаем переменные окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_panel.settings')
django.setup()