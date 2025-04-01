from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db import get_user
from utils.zodiac import get_zodiac_sign


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
        user = await get_user(callback.from_user.id)
    
        if user and user[3]:  # user[3] = birth_date
            try:
                day, month, *_ = map(int, user[3].split("."))
                sign = get_zodiac_sign(day, month)
                text = f"🆓 Гороскоп на сегодня для знака {sign}:\n\n🌞 Этот день принесёт новые возможности и ясность."
            except:
                text = "Не удалось определить знак зодиака. Проверь дату в профиле."
        else:
            text = "🆓 Чтобы получить гороскоп, выбери свой знак зодиака:"
            keyboard = InlineKeyboardMarkup(row_width=2)
            signs = [
                "Овен", "Телец", "Близнецы", "Рак",
                "Лев", "Дева", "Весы", "Скорпион",
                "Стрелец", "Козерог", "Водолей", "Рыбы"
            ]
            for sign in signs:
                keyboard.insert(InlineKeyboardButton(sign, callback_data=f"free_horoscope_{sign.lower()}"))
            keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data="menu_horoscope"))
            await callback.message.edit_text(text, reply_markup=keyboard)
            await callback.answer()
            return
    
        await callback.message.edit_text(text, reply_markup=horoscope_menu_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data.startswith("free_horoscope_"))
    async def horoscope_by_sign(callback: types.CallbackQuery):
        sign = callback.data.split("_")[-1].capitalize()
        text = f"🆓 Гороскоп на сегодня для знака {sign}:\n\n🌟 День подойдёт для внутреннего роста и спокойствия."
        await callback.message.edit_text(text, reply_markup=horoscope_menu_keyboard())
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
