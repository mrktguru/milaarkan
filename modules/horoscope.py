from aiogram import types
from aiogram.dispatcher import Dispatcher

def setup(dp: Dispatcher):
    @dp.message_handler(lambda message: message.text == "🔮 Гороскоп")
    async def horoscope_menu(message: types.Message):
        text = (
            "Каждый день — как новый разворот личной книги жизни.\n"
            "Выбери вариант гороскопа:"
        )
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            "🆓 Гороскоп на сегодня", "📆 Гороскоп на неделю",
            "💫 Персональный гороскоп", "🔙 Назад"
        ]
        keyboard.add(*buttons)
        await message.answer(text, reply_markup=keyboard)
