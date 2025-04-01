import logging
import os
from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv

from utils.db import init_db

if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(init_db())  # инициализируем БД
    executor.start_polling(dp, skip_updates=True)


# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN не задан в .env файле.")

# Настройка логирования и инициализация бота
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Импорт модулей (обработчики)
from modules import main_menu, horoscope, tarot, energy, profile, about

# Регистрация обработчиков модулей
main_menu.setup(dp)
horoscope.setup(dp)
tarot.setup(dp)
energy.setup(dp)
profile.setup(dp)
about.setup(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
