import logging
import os
from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Инициализация хранилища и диспетчера
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Загрузка переменных из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN не найден в .env")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Импорт модулей
from modules import main_menu, horoscope, tarot, energy, profile, about
from utils.db import init_db

# Подключаем обработчики
main_menu.setup(dp)
horoscope.setup(dp)
tarot.setup(dp)
energy.setup(dp)
profile.setup(dp)
about.setup(dp)

# Запуск бота
if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(init_db())  # инициализация БД
    executor.start_polling(dp, skip_updates=True)
