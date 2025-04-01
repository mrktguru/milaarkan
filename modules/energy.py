from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_energy")
    async def energy_menu(callback: types.CallbackQuery):
        text = (
            "💎 Энергия\n\n"
            "Энергия — это мой личный ресурс, который я вкладываю в работу с тобой: гороскопы, расклады, ответы на важные вопросы.\n\n"
            "Выбери, что тебе нужно:"
        )
        await callback.message.edit_text(text, reply_markup=energy_menu_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "energy_balance")
    async def show_balance(callback: types.CallbackQuery):
        # Пример: можно заменить на реальный расчёт
        energy = 150
        await callback.message.edit_text(
            f"✨ Сейчас у тебя: {energy} энергии.\n\nТы можешь пополнить её или получить бонус.",
            reply_markup=energy_menu_keyboard()
        )
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "energy_buy")
    async def buy_energy(callback: types.CallbackQuery):
        text = "🛒 Пополнение энергии\n\nВыбери подходящий пакет:"
        keyboard = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("100 энергии — 99 ₽", callback_data="pay_100"),
            InlineKeyboardButton("300 энергии — 249 ₽", callback_data="pay_300"),
            InlineKeyboardButton("1000 энергии — 599 ₽", callback_data="pay_1000"),
            InlineKeyboardButton("🔙 Назад", callback_data="menu_energy")
        )
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "energy_bonus")
    async def get_bonus(callback: types.CallbackQuery):
        text = (
            "🎁 Получить бонус\n\n"
            "Ты можешь получить:\n"
            "• +10 энергии ежедневно\n"
            "• +50% от оплаты друга\n"
            "• Сюрприз дня — случайный бонус\n\n"
            "✨ Делись и возвращайся!"
        )
        await callback.message.edit_text(text, reply_markup=energy_menu_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "energy_history")
    async def show_history(callback: types.CallbackQuery):
        # Пример (в будущем подгрузка из БД)
        text = (
            "📖 История энергии\n\n"
            "• 30.03 — Персональный гороскоп — -300 энергии\n"
            "• 29.03 — Пригласил друга — +150 энергии\n"
            "• 28.03 — Карта дня — -50 энергии\n"
        )
        await callback.message.edit_text(text, reply_markup=energy_menu_keyboard())
        await callback.answer()

def energy_menu_keyboard():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("✨ Мой баланс", callback_data="energy_balance"),
        InlineKeyboardButton("🛒 Пополнить энергию", callback_data="energy_buy"),
        InlineKeyboardButton("🎁 Получить бонус", callback_data="energy_bonus"),
        InlineKeyboardButton("📖 История трат", callback_data="energy_history"),
        InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
    )
