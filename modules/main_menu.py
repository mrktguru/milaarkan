from aiogram import types
from aiogram.dispatcher import Dispatcher

def setup(dp: Dispatcher):
    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        welcome_text = (
            "Здравствуй.\n"
            "Меня зовут Мила Аркан, я астролог и практикующий психолог.\n\n"
            "Если ты здесь — это не случайность. Иногда судьба проявляется через детали: нужный человек, вовремя прочитанное сообщение… или вот такой бот.\n\n"
            "Я помогу тебе понять, что происходит внутри и снаружи — через язык звёзд и символов.\n\n"
            "🌿 Готова начать?"
        )
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("🔮 Гороскоп")
        keyboard.add("🃏 Таро-расклад")
        keyboard.add("💎 Моя энергия")
        keyboard.add("🧘 Профиль")
        keyboard.add("📖 Обо мне")
        keyboard.add("✉️ Задать вопрос")
        await message.answer(welcome_text, reply_markup=keyboard)
