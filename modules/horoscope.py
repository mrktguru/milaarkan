from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_horoscope")
    async def show_horoscope_menu(callback: types.CallbackQuery):
        text = (
            "🔮 Гороскопы\n\n"
            "Каждый день — как новый разворот личной книги жизни.\n"
            "Выбери формат:"
        )
        await callback.message.edit_text(text, reply_markup=horoscope_menu_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "horoscope_today")
    async def horoscope_today(callback: types.CallbackQuery):
        await callback.message.edit_text("🆓 Гороскоп на сегодня:\n\n🌞 День подойдёт для лёгких задач и внутреннего фокуса.", reply_markup=horoscope_menu_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "horoscope_week")
    async def horoscope_week(callback: types.CallbackQuery):
        await callback.message.edit_text("📆 Гороскоп на неделю:\n\n🔄 Неделя подойдёт для пересмотра целей и работы с отношениями.", reply_markup=horoscope_menu_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "horoscope_personal")
    async def horoscope_personal(callback: types.CallbackQuery):
        await callback.message.edit_text(
            "💫 Персональный гороскоп доступен по твоей астрологической карте.\n\n"
            "Чтобы я смогла его составить, заполни профиль и пополни энергию.\n"
            "Расчёт производится вручную и занимает от 2 до 5 часов.",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("🧘 Перейти к профилю", callback_data="menu_profile"),
                InlineKeyboardButton("💎 Пополнить энергию", callback_data="menu_energy"),
                InlineKeyboardButton("🔙 Назад", callback_data="menu_horoscope")
            )
        )
        await callback.answer()

def horoscope_menu_keyboard():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("🆓 Гороскоп на сегодня", callback_data="horoscope_today"),
        InlineKeyboardButton("📆 Гороскоп на неделю", callback_data="horoscope_week"),
        InlineKeyboardButton("💫 Персональный гороскоп", callback_data="horoscope_personal"),
        InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
    )
