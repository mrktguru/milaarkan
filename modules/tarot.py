from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_tarot")
    async def show_tarot_menu(callback: types.CallbackQuery):
        text = (
            "🃏 Таро-расклады\n\n"
            "Карты — это способ услышать внутренний голос.\n"
            "Выбери формат, который откликается тебе сейчас:"
        )
        await callback.message.edit_text(text, reply_markup=tarot_menu_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data.startswith("tarot_"))
    async def show_tarot_info(callback: types.CallbackQuery):
        texts = {
            "tarot_day": "🃏 Карта дня — 50 энергии\n\nОдин символ. Один акцент. Подсказка, на чём сфокусироваться в течение дня.",
            "tarot_compass": "🌿 Внутренний компас — 100 энергии\n\nПрошлое — Настоящее — Будущее. Помогает почувствовать, где ты и куда направляется твоя энергия.",
            "tarot_love": "❤️ Отношения — 250 энергии\n\nТы — Он/Она — Что вас соединяет — Что мешает — Возможный вектор.",
            "tarot_action": "💼 Моя ситуация — 250 энергии\n\nСуть запроса — влияние — скрытые импульсы — возможный результат — совет.",
            "tarot_free": "🔮 Свободный вопрос — 300 энергии\n\nТы задаёшь вопрос — карта отвечает образом, через который приходит подсказка."
        }

        back_btn = InlineKeyboardButton("🔙 Назад", callback_data="menu_tarot")
        data_key = callback.data
        await callback.message.edit_text(
            texts.get(data_key, "Расклад не найден."),
            reply_markup=InlineKeyboardMarkup().add(back_btn)
        )
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
