import logging
import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN не найден в .env")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание бота
bot = Bot(token=BOT_TOKEN)

# Подключение FSM-хранилища
storage = MemoryStorage()

# Диспетчер с хранилищем FSM
dp = Dispatcher(bot, storage=storage)

# Импорт модулей
from modules import main_menu, horoscope, tarot, energy, profile, about
from utils.db import init_db

# Подключение обработчиков
main_menu.setup(dp)
horoscope.setup(dp)
tarot.setup(dp)
energy.setup(dp)
profile.setup(dp)
about.setup(dp)

# Запуск бота
if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(init_db())  # Инициализация базы данных
    executor.start_polling(dp, skip_updates=True)
