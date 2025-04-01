from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.time_status import online_status_text


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

    @dp.callback_query_handler(lambda c: c.data == "noop_status")
    async def ignore_status_click(callback: types.CallbackQuery):
        if is_mila_online():
            text = "Мила сейчас онлайн и готова быть рядом, если ты захочешь обратиться 🌿"
        else:
            text = "Сейчас Мила не в сети. Но как только появится — обязательно ответит тебе."
        await callback.answer(text, show_alert=False)



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
    # Добавим статусную кнопку в самом низу
    status = online_status_text()
    keyboard.add(InlineKeyboardButton(status, callback_data="noop_status"))
    return keyboard

