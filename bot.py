import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("⚠️ BOT_TOKEN не найден в .env файле")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# ===== Модули =====
from modules import main_menu, horoscope, tarot, energy, profile, about, placeholders
from utils.db import init_db


# ===== Подключаем handlers =====
main_menu.setup(dp)
horoscope.setup(dp)
tarot.setup(dp)
energy.setup(dp)
profile.setup(dp)
about.setup(dp)
placeholders.setup(dp)


# ===== Startup: инициализация БД =====
async def on_startup(dispatcher):
    await init_db()
    logging.info("Бот запущен и база данных инициализирована.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
