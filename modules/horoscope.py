from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import pytz

from utils.db import get_user, save_user_action, get_user_energy, update_user_energy
from utils.zodiac import get_zodiac_sign
from utils.gpt import generate_horoscope_for_sign, generate_weekly_horoscope
from modules.main_menu import show_main_menu


HOROSCOPE_PRICE = 50

def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_horoscope")
    async def show_horoscope_menu(callback: types.CallbackQuery):
        text = (
            "Каждый день — как новый разворот личной книги жизни.\n"
            "Выбери формат гороскопа:"
        )
        keyboard = horoscope_menu_keyboard()
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()

    async def is_today_used(user_id: int) -> bool:
        tz = pytz.timezone("Europe/Moscow")
        today = datetime.now(tz).strftime("%Y-%m-%d")
        return await save_user_action(user_id, action="daily_horoscope", date=today, check_only=True)

    @dp.callback_query_handler(lambda c: c.data == "horoscope_today")
    async def horoscope_today(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        user = await get_user(user_id)

        if await is_today_used(user_id):
            keyboard = InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton("🔮 Да, покажи на завтра", callback_data="horoscope_tomorrow"),
                InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
            )
            await callback.message.edit_text(
                "Гороскоп на сегодня я уже создала для тебя 🌙\n\n"
                "Я не повторяюсь — ведь энергия момента уже была прочувствована.\n"
                "Но если хочешь — могу почувствовать завтрашний день заранее.\n\n"
                "🌿 Как тебе такой вариант?",
                reply_markup=keyboard
            )
            return

        energy = await get_user_energy(user_id)
        if energy < HOROSCOPE_PRICE:
            await callback.message.edit_text(
                f"⛔ У тебя недостаточно энергии.\n\nДля гороскопа нужно {HOROSCOPE_PRICE}, а у тебя — {energy}.\n"
                "Пополни баланс в разделе «Энергия».",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("💎 Пополнить энергию", callback_data="menu_energy"),
                    InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
                )
            )
            return

        await update_user_energy(user_id, -HOROSCOPE_PRICE)
        await save_user_action(user_id, action="daily_horoscope")

        if user and user[3]:
            day, month, *_ = map(int, user[3].split("."))
            sign = get_zodiac_sign(day, month)
            await callback.message.edit_text(f"✨ Мила настраивается на твой знак... {sign} ♡\nПодожди немного…")

            horoscope_parts = await generate_horoscope_for_sign(
                sign, personal=True, name=user[2]
            )

            await callback.message.edit_text(
                f"🌿 {sign}: гороскоп на сегодня\n\n{horoscope_parts[0]}",
                reply_markup=horoscope_menu_keyboard()
            )

            for part in horoscope_parts[1:]:
                await callback.message.answer(part)
        else:
            await callback.message.edit_text(
                "У тебя не заполнен профиль. Пожалуйста, укажи дату рождения — я подскажу твой знак зодиака.",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("🧬 Заполнить профиль", callback_data="menu_profile"),
                    InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
                )
            )

        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "horoscope_tomorrow")
    async def horoscope_tomorrow(callback: types.CallbackQuery):
        user = await get_user(callback.from_user.id)
        if user and user[3]:
            day, month, *_ = map(int, user[3].split("."))
            sign = get_zodiac_sign(day, month)
            await callback.message.edit_text(f"✨ Мила настраивается на завтрашний день для {sign} ♡")

            horoscope_parts = await generate_horoscope_for_sign(
                sign, period="завтра", personal=True, name=user[2]
            )

            await callback.message.edit_text(
                f"🌿 {sign}: гороскоп на завтра\n\n{horoscope_parts[0]}",
                reply_markup=horoscope_menu_keyboard()
            )

            for part in horoscope_parts[1:]:
                await callback.message.answer(part)
        else:
            await callback.message.edit_text(
                "Чтобы я могла рассчитать завтрашний гороскоп — нужно заполнить профиль 💫",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("🧬 Заполнить профиль", callback_data="menu_profile"),
                    InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
                )
            )

    @dp.callback_query_handler(lambda c: c.data == "horoscope_week")
    async def horoscope_week(callback: types.CallbackQuery):
        user = await get_user(callback.from_user.id)

        if user and user[3]:
            try:
                day, month, *_ = map(int, user[3].split("."))
                sign = get_zodiac_sign(day, month)
                await callback.message.edit_text(f"✨ Мила настраивается на неделю для знака {sign}…\nПодожди немного 🌿")

                horoscope_parts = await generate_weekly_horoscope(
                    sign,
                    personal=True,
                    name=user[2]
                )

                await callback.message.edit_text(
                    f"📆 Гороскоп на неделю для {sign}:\n\n{horoscope_parts[0]}",
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
            await callback.message.edit_text(
                "У тебя не заполнен профиль. Пожалуйста, укажи дату рождения, чтобы я могла определить твой знак 🌿",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("🧬 Заполнить профиль", callback_data="menu_profile"),
                    InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
                )
            )

    @dp.callback_query_handler(lambda c: c.data == "horoscope_personal")
    async def horoscope_personal(callback: types.CallbackQuery):
        text = (
            "💫 Персональный гороскоп — это не просто текст.\n"
            "Это внимательная ручная работа, которую я создаю на основе твоей натальной карты: даты, времени и места рождения.\n\n"
            "На её составление уходит от 2 до 5 часов. Но главное — он раскрывает именно твою ситуацию, энергии и возможности.\n\n"
            "Такой гороскоп помогает не только понять, но и почувствовать — что сейчас важно именно для тебя."
        )
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
        )
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "main_menu")
    async def back_to_main(callback: types.CallbackQuery):
        await show_main_menu(callback)


def horoscope_menu_keyboard():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("🆓 На сегодня", callback_data="horoscope_today"),
        InlineKeyboardButton("📆 На неделю", callback_data="horoscope_week"),
        InlineKeyboardButton("💫 Персональный", callback_data="horoscope_personal"),
        InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
    )
