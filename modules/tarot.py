from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.time_status import is_mila_online, online_status_text

def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_tarot")
    async def show_tarot_menu(callback: types.CallbackQuery):
        text = (
            "🃏 Таро-расклады\n\n"
            "Иногда, чтобы прояснить ситуацию, достаточно правильно задать вопрос внутри.\n\n"
            "Выбери расклад, который откликается тебе сейчас:"
        )
        await callback.message.edit_text(text, reply_markup=tarot_menu_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data.startswith("tarot_"))
    async def show_tarot_info(callback: types.CallbackQuery):
        data_key = callback.data
        status = online_status_text()

        texts = {
            "tarot_day": f"{status}\n\n🃏 Карта дня — 50 энергии\n\nСконцентрируйся. Один символ. Один акцент.",
            "tarot_compass": f"{status}\n\n🌿 Внутренний компас — 100 энергии\n\nПрошлое — Настоящее — Будущее.",
            "tarot_love": f"{status}\n\n❤️ Отношения — 250 энергии\n\nТы — Он/Она — Что вас соединяет…",
            "tarot_action": f"{status}\n\n💼 Моя ситуация — 250 энергии\n\nСуть запроса — влияние — результат.",
            "tarot_free": f"{status}\n\n🔮 Свободный вопрос — 300 энергии\n\nТы задаёшь вопрос — карта отвечает."
        }

        text = texts.get(data_key, "Расклад не найден.")
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔙 Назад", callback_data="menu_tarot")
        )

        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()

def tarot_menu_keyboard():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("🃏 Карта дня — 50", callback_data="tarot_day"),
        InlineKeyboardButton("🌿 Внутренний компас — 100", callback_data="tarot_compass"),
        InlineKeyboardButton("❤️ Отношения — 250", callback_data="tarot_love"),
        InlineKeyboardButton("💼 Моя ситуация — 250", callback_data="tarot_action"),
        InlineKeyboardButton("🔮 Свободный вопрос — 300", callback_data="tarot_free"),
        InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
    )
