from aiogram import types
from aiogram.dispatcher import Dispatcher

def setup(dp: Dispatcher):
    @dp.message_handler(lambda message: message.text == "📖 Обо мне")
    async def about_menu(message: types.Message):
        text = (
            "Приветствую. Я — Мила Аркан, астролог и практикующий психолог.\n\n"
            "Уже более 10 лет я помогаю людям понимать себя и окружающий мир через язык звёзд, символов и интуиции.\n\n"
            "Моя цель — создать пространство для глубокого самоанализа, где каждый может найти поддержку и понимание.\n"
            "Если ты здесь, значит, ты ищешь ответы и хочешь открыть для себя новые грани своей души."
        )
        await message.answer(text)
