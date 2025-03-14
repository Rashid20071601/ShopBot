# Импорт библиотек
from aiogram.dispatcher.filters.state import State, StatesGroup
import os
import sys
import django
from logging_config import setup_logger


# Настраиваем логгер
logger = setup_logger()

# Определяем состояния
class UserRegistration(StatesGroup):
    waiting_for_email = State()
    waiting_for_phone = State()

class CartState(StatesGroup):
    waiting_for_product_id = State()

# Получаем путь к корневой директории проекта (ShopBot)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)  # Добавляем корневую директорию проекта

# Логируем добавление пути в sys.path
logger.info(f"Добавлен путь в sys.path: {BASE_DIR}")

# Добавляем `admin_panel` в sys.path
ADMIN_PANEL_DIR = os.path.join(BASE_DIR, "admin_panel")
sys.path.append(ADMIN_PANEL_DIR)

# Логируем добавление пути admin_panel в sys.path
logger.info(f"Добавлен путь admin_panel в sys.path: {ADMIN_PANEL_DIR}")

# Устанавливаем переменные окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_panel.settings')

# Логируем установку переменной окружения Django
logger.info(f"Установлена переменная окружения DJANGO_SETTINGS_MODULE: {os.environ['DJANGO_SETTINGS_MODULE']}")

# Инициализация Django
django.setup()

# Логируем успешную инициализацию Django
logger.info("Django успешно инициализирован.")