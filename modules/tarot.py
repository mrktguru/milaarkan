from aiogram import types
from aiogram.dispatcher import Dispatcher

def setup(dp: Dispatcher):
    @dp.message_handler(lambda message: message.text == "🃏 Таро-расклад")
    async def tarot_menu(message: types.Message):
        text = (
            "Иногда, чтобы прояснить ситуацию, достаточно правильно задать вопрос внутри.\n"
            "Выбери нужный расклад:"
        )
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            "🃏 Карта дня", "🌿 Внутренний компас",
            "❤️ Отношения: что между нами?", "💼 Моя ситуация: как поступить?",
            "🔮 Свободный вопрос к Таро", "🔙 Назад"
        ]
        keyboard.add(*buttons)
        await message.answer(text, reply_markup=keyboard)
