from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.time_status import is_mila_online


def main_menu_keyboard():
    status = "🟢 Мила в сети" if is_mila_online() else "🔘 Мила не в сети"
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("🔮 Гороскоп", callback_data="menu_horoscope"),
        InlineKeyboardButton("🃏 Таро-расклады", callback_data="menu_tarot"),
        InlineKeyboardButton("💎 Энергия", callback_data="menu_energy"),
        InlineKeyboardButton("🧬 Профиль", callback_data="menu_profile"),
        InlineKeyboardButton("📖 Обо мне", callback_data="menu_about"),
        InlineKeyboardButton(status, callback_data="mila_status")
    )


async def show_main_menu(callback_or_message):
    text = (
        "Здравствуй.\n"
        "Меня зовут Мила Аркан, я астролог и практикующий психолог.\n\n"
        "Если ты здесь — это не случайность. Иногда судьба проявляется через детали: нужный человек, вовремя прочитанное сообщение… или вот такой бот.\n\n"
        "Я помогу тебе понять, что происходит внутри и снаружи — через язык звёзд и символов.\n\n"
        "🌿 Готова начать?"
    )
    keyboard = main_menu_keyboard()

    if isinstance(callback_or_message, types.CallbackQuery):
        await callback_or_message.message.edit_text(text, reply_markup=keyboard)
        await callback_or_message.answer()
    elif isinstance(callback_or_message, types.Message):
        await callback_or_message.answer(text, reply_markup=keyboard)


def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "start")
    async def handle_start(callback: types.CallbackQuery):
        await show_main_menu(callback)

    @dp.message_handler(commands=["start"])
    async def handle_start_cmd(message: types.Message):
        await show_main_menu(message)

    @dp.callback_query_handler(lambda c: c.data == "main_menu")
    async def handle_main_menu(callback: types.CallbackQuery):
        await show_main_menu(callback)

    @dp.callback_query_handler(lambda c: c.data == "mila_status")
    async def ignore_status_click(callback: types.CallbackQuery):
        if is_mila_online():
            await callback.answer("Мила онлайн и готова помочь тебе 🌿", show_alert=False)
        else:
            await callback.answer("Милы сейчас нет в сети. Как будет — сразу почувствует тебя ✨", show_alert=False)
