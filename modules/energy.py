from aiogram import types
from aiogram.dispatcher import Dispatcher

def setup(dp: Dispatcher):
    @dp.message_handler(lambda message: message.text == "💎 Моя энергия")
    async def energy_menu(message: types.Message):
        text = (
            "Энергия — это мой личный ресурс, который я вкладываю в работу с тобой.\n"
            "Проверь свой баланс или пополни его, чтобы продолжать получать услуги."
        )
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            "✨ Мой баланс", "🛒 Пополнить энергию",
            "🎁 Получить бонус", "📖 История трат", "🔙 Назад"
        ]
        keyboard.add(*buttons)
        await message.answer(text, reply_markup=keyboard)
