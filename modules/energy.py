from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules.main_menu import show_main_menu


def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_energy")
    async def show_energy_menu(callback: types.CallbackQuery):
        text = (
            "Энергия — это мой личный ресурс, который я вкладываю в работу с тобой.\n\n"
            "Каждый гороскоп, каждый расклад — это не автоматический текст, а реальная работа, "
            "которая требует внимания, сил и тишины.\n\n"
            "Выбери, что тебе нужно:"
        )
        await callback.message.edit_text(text, reply_markup=energy_menu_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "energy_buy")
    async def energy_buy(callback: types.CallbackQuery):
        await callback.message.edit_text("Выбери удобный пакет пополнения:", reply_markup=buy_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "energy_history")
    async def energy_history(callback: types.CallbackQuery):
        await callback.message.edit_text("Здесь ты можешь увидеть, как использовалась твоя энергия.", reply_markup=energy_menu_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "energy_bonus")
    async def energy_bonus(callback: types.CallbackQuery):
        text = "• Пригласи друга — 20 энергии (после его оплаты)\n• Или получи 50% его первого пополнения на свой баланс"
        await callback.message.edit_text(text, reply_markup=energy_menu_keyboard())
        await callback.answer()

def energy_menu_keyboard():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("🛒 Пополнить энергию", callback_data="energy_buy"),
        InlineKeyboardButton("📖 История трат", callback_data="energy_history"),
        InlineKeyboardButton("🎁 Получить бонус", callback_data="energy_bonus"),
        InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
    )

def buy_keyboard():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("💎 100 энергии — 99 ₽", callback_data="pay_100"),
        InlineKeyboardButton("💎 300 энергии — 249 ₽", callback_data="pay_300"),
        InlineKeyboardButton("💎 1000 энергии — 699 ₽", callback_data="pay_1000"),
        InlineKeyboardButton("🔙 Назад", callback_data="menu_energy")
    )

    @dp.callback_query_handler(lambda c: c.data == "main_menu")
    async def back_to_main(callback: types.CallbackQuery):
        await show_main_menu(callback)
