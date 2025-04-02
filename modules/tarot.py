from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules.main_menu import show_main_menu


def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_tarot")
    async def show_tarot_menu(callback: types.CallbackQuery):
        text = (
            "🃏 Карты Таро — это отражение твоего внутреннего мира.\n"
            "Сконцентрируйся и задай вопрос. Я помогу прочитать то, что подсказывает твоя интуиция."
        )
        keyboard = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("🔹 Карта дня", callback_data="tarot_day"),
            InlineKeyboardButton("💬 Моя ситуация", callback_data="tarot_situation"),
            InlineKeyboardButton("❤️ Отношения", callback_data="tarot_love"),
            InlineKeyboardButton("🔍 Свободный вопрос", callback_data="tarot_custom"),
            InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
        )
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()

    # Пример одного из раскладов
    @dp.callback_query_handler(lambda c: c.data == "tarot_day")
    async def tarot_day(callback: types.CallbackQuery):
        text = (
            "Сконцентрируйся. Спроси себя — что важно для меня прямо сейчас?\n"
            "Когда почувствуешь — нажми, и я открою карту для тебя."
        )
        keyboard = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("🔮 Открыть карту", callback_data="tarot_draw_card"),
            InlineKeyboardButton("🔙 Назад", callback_data="menu_tarot")
        )
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()

    # Общий обработчик возврата в главное меню
    @dp.callback_query_handler(lambda c: c.data == "main_menu")
    async def back_to_main(callback: types.CallbackQuery):
        await show_main_menu(callback)
