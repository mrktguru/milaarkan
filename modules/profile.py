from aiogram import types
from aiogram.dispatcher import Dispatcher

def setup(dp: Dispatcher):
    @dp.message_handler(lambda message: message.text == "🧘 Профиль")
    async def profile_menu(message: types.Message):
        text = (
            "Здесь ты создаёшь свой личный профиль, который помогает мне лучше понимать твои потребности.\n"
            "Заполни или отредактируй данные, чтобы мы могли глубже заглянуть в твой мир."
        )
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["✏️ Изменить данные", "🔙 Назад"]
        keyboard.add(*buttons)
        await message.answer(text, reply_markup=keyboard)
