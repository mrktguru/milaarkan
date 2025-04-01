from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def setup(dp: Dispatcher):

    @dp.message_handler(commands=["start"])
    async def send_welcome(message: types.Message):
        text = (
            "Здравствуй.\n"
            "Меня зовут Мила Аркан, я астролог и практикующий психолог.\n\n"
            "Если ты здесь — это не случайность. Иногда судьба проявляется через детали: нужный человек, вовремя прочитанное сообщение… или вот такой бот.\n\n"
            "Я помогу тебе понять, что происходит внутри и снаружи — через язык звёзд и символов.\n\n"
            "🌿 Готова начать?"
        )
        await message.answer(text, reply_markup=main_menu_keyboard())

    @dp.callback_query_handler(lambda c: c.data == "main_menu")
    async def return_to_main_menu(callback: types.CallbackQuery):
        text = (
            "Здравствуй.\n"
            "Меня зовут Мила Аркан, я астролог и практикующий психолог.\n\n"
            "Если ты здесь — это не случайность. Иногда судьба проявляется через детали: нужный человек, вовремя прочитанное сообщение… или вот такой бот.\n\n"
            "Я помогу тебе понять, что происходит внутри и снаружи — через язык звёзд и символов.\n\n"
            "🌿 Готова начать?"
        )
        await callback.message.edit_text(text, reply_markup=main_menu_keyboard())
        await callback.answer()


def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🔮 Гороскоп", callback_data="menu_horoscope"),
        InlineKeyboardButton("🃏 Таро-расклад", callback_data="menu_tarot"),
        InlineKeyboardButton("💎 Моя энергия", callback_data="menu_energy"),
        InlineKeyboardButton("🧘 Профиль", callback_data="menu_profile"),
        InlineKeyboardButton("📖 Обо мне", callback_data="menu_about"),
        InlineKeyboardButton("✉️ Задать вопрос", callback_data="menu_question")
    )
    return keyboard
