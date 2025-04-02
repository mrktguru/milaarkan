from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db import get_user
from utils.zodiac import get_zodiac_sign
from utils.gpt import generate_horoscope_for_sign


def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_horoscope")
    async def show_horoscope_menu(callback: types.CallbackQuery):
        text = (
            "Каждый день — как новый разворот личной книги жизни.\n"
            "Выбери формат гороскопа:"
        )
        keyboard = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("🆓 На сегодня", callback_data="horoscope_today"),
            InlineKeyboardButton("📆 На неделю", callback_data="horoscope_week"),
            InlineKeyboardButton("💫 Персональный", callback_data="horoscope_personal"),
            InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
        )
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "horoscope_today")
    async def horoscope_today(callback: types.CallbackQuery):
        user = await get_user(callback.from_user.id)
        if user and user[3]:
            try:
                day, month, *_ = map(int, user[3].split("."))
                sign = get_zodiac_sign(day, month)
                await callback.message.edit_text(f"✨ Мила настраивается на твой знак... {sign} ♡\nПодожди немного…")

                horoscope_parts = await generate_horoscope_for_sign(
                    sign,
                    personal=True,
                    name=user[2]
                )

                await callback.message.edit_text(
                    f"🌿 Гороскоп на сегодня для {sign}:\n\n{horoscope_parts[0]}",
                    reply_markup=horoscope_menu_keyboard()
                )

                for part in horoscope_parts[1:]:
                    await callback.message.answer(part)

            except:
                await callback.message.edit_text(
                    "Не удалось определить знак зодиака. Проверь дату рождения в профиле.",
                    reply_markup=horoscope_menu_keyboard()
                )
        else:
            text = "🆓 Чтобы получить гороскоп, выбери свой знак зодиака:"
            keyboard = InlineKeyboardMarkup(row_width=2)
            signs = [
                ("♈ Овен", "21.03–19.04"),
                ("♉ Телец", "20.04–20.05"),
                ("♊ Близнецы", "21.05–20.06"),
                ("♋ Рак", "21.06–22.07"),
                ("♌ Лев", "23.07–22.08"),
                ("♍ Дева", "23.08–22.09"),
                ("♎ Весы", "23.09–22.10"),
                ("♏ Скорпион", "23.10–21.11"),
                ("♐ Стрелец", "22.11–21.12"),
                ("♑ Козерог", "22.12–19.01"),
                ("♒ Водолей", "20.01–18.02"),
                ("♓ Рыбы", "19.02–20.03"),
            ]
            for sign, dates in signs:
                sign_clean = sign.split(" ")[1].lower()
                keyboard.insert(
                    InlineKeyboardButton(f"{sign} ({dates})", callback_data=f"free_horoscope_{sign_clean}")
                )
            keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data="menu_horoscope"))
            await callback.message.edit_text(text, reply_markup=keyboard)

        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data.startswith("free_horoscope_"))
    async def horoscope_by_sign(callback: types.CallbackQuery):
        sign = callback.data.split("_")[-1].capitalize()
        await callback.message.edit_text(f"✨ Мила настраивается на твой знак... {sign} ♡\nПодожди немного…")

        horoscope_parts = await generate_horoscope_for_sign(sign, personal=False)

        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔙 Назад", callback_data="menu_horoscope")
        )

        await callback.message.edit_text(
            f"🌿 Гороскоп на сегодня для {sign}:\n\n{horoscope_parts[0]}", reply_markup=keyboard
        )

        for part in horoscope_parts[1:]:
            await callback.message.answer(part)

        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "horoscope_week")
    async def horoscope_week(callback: types.CallbackQuery):
        await callback.message.edit_text(
            "📆 Гороскоп на неделю:\n\n🔄 Неделя подойдёт для пересмотра целей и работы с отношениями.",
            reply_markup=horoscope_menu_keyboard()
        )
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "horoscope_personal")
    async def horoscope_personal(callback: types.CallbackQuery):
        text = (
            "💫 Персональный гороскоп — это не просто текст.\n"
            "Это внимательная ручная работа, которую я создаю на основе твоей натальной карты: даты, времени и места рождения.\n\n"
            "На её составление уходит от 2 до 5 часов. Но главное — он раскрывает именно твою ситуацию, энергии и возможности.\n\n"
            "Такой гороскоп помогает не только понять, но и почувствовать — что сейчас важно именно для тебя."
        )
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔙 Назад", callback_data="menu_horoscope")
        )
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()

def horoscope_menu_keyboard():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("🆓 На сегодня", callback_data="horoscope_today"),
        InlineKeyboardButton("📆 На неделю", callback_data="horoscope_week"),
        InlineKeyboardButton("💫 Персональный", callback_data="horoscope_personal"),
        InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
    )
