from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

from utils.db import save_user_profile, get_user
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="milaarkan_bot")


class ProfileForm(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_city = State()
    confirm_city = State()


def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_profile")
    async def show_profile(callback: types.CallbackQuery):
        user = await get_user(callback.from_user.id)
        if user and all(user[2:6]):
            text = (
                f"👤 Твой профиль:\n\n"
                f"Имя: {user[2]}\n"
                f"Дата рождения: {user[3]}\n"
                f"Время рождения: {user[4]}\n"
                f"Город: {user[5]}"
            )
        else:
            text = (
                "🌿 Чтобы я могла создавать персональные гороскопы, мне нужно немного узнать о тебе.\n"
                "Давай заполним твой профиль."
            )

        keyboard = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("✏️ Заполнить / Изменить", callback_data="edit_profile"),
            InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
        )
        await callback.message.edit_text(text, reply_markup=keyboard)

    @dp.callback_query_handler(lambda c: c.data == "edit_profile")
    async def start_profile_edit(callback: types.CallbackQuery, state: FSMContext):
        await state.finish()
        await callback.message.edit_text("Как тебя зовут? Только буквы, без цифр.")
        await ProfileForm.name.set()

    @dp.message_handler(state=ProfileForm.name)
    async def fsm_name(message: types.Message, state: FSMContext):
        if not re.match(r"^[А-Яа-яA-Za-zёЁ\s\-]{2,}$", message.text):
            await message.answer("🌿 Я чувствую, что имя — это что-то большее, чем набор символов.\nПожалуйста, напиши его без цифр и знаков.")
            return
        await state.update_data(name=message.text.strip())
        await message.answer("🗓 Введи дату рождения в формате ДД.ММ.ГГГГ (например: 07.04.1992)")
        await ProfileForm.birth_date.set()

    @dp.message_handler(state=ProfileForm.birth_date)
    async def fsm_birth_date(message: types.Message, state: FSMContext):
        if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", message.text):
            await message.answer("📅 Чтобы всё получилось точно — напиши дату вот так: 07.04.1992")
            return
        await state.update_data(birth_date=message.text.strip())
        await message.answer("⏰ Введи время рождения в формате ЧЧ:ММ (например: 14:30)")
        await ProfileForm.birth_time.set()

    @dp.message_handler(state=ProfileForm.birth_time)
    async def fsm_birth_time(message: types.Message, state: FSMContext):
        if not re.match(r"^\d{2}:\d{2}$", message.text):
            await message.answer("⏳ Пожалуйста, укажи время в формате: 14:30")
            return
        await state.update_data(birth_time=message.text.strip())
        await message.answer("🏙 Введи город рождения")
        await ProfileForm.birth_city.set()

    @dp.message_handler(state=ProfileForm.birth_city)
    async def fsm_birth_city(message: types.Message, state: FSMContext):
        city = message.text.strip()
        location = geolocator.geocode(city)
        if location:
            await state.update_data(birth_city=city)
            return await save_and_show_profile(message, state)
        else:
            await state.update_data(birth_city=city)
            keyboard = InlineKeyboardMarkup().add(
                InlineKeyboardButton("✅ Подтвердить город", callback_data="confirm_city"),
                InlineKeyboardButton("🔁 Ввести другой", callback_data="edit_profile")
            )
            await message.answer(
                "🌍 Я не нашла такой город. Возможно, в написании есть ошибка?\n"
                "Если уверена — нажми 'Подтвердить', и я доверюсь тебе.", reply_markup=keyboard)
            await ProfileForm.confirm_city.set()

    @dp.callback_query_handler(lambda c: c.data == "confirm_city", state=ProfileForm.confirm_city)
    async def fsm_confirm_city(callback: types.CallbackQuery, state: FSMContext):
        await save_and_show_profile(callback.message, state)
        await state.finish()

    async def save_and_show_profile(message: types.Message, state: FSMContext):
        data = await state.get_data()
        await save_user_profile(
            telegram_id=message.from_user.id,
            name=data.get("name"),
            birth_date=data.get("birth_date"),
            birth_time=data.get("birth_time"),
            birth_city=data.get("birth_city")
        )
        text = (
            "💫 Спасибо. Профиль сохранён.\n\n"
            f"Имя: {data.get('name')}\n"
            f"Дата рождения: {data.get('birth_date')}\n"
            f"Время рождения: {data.get('birth_time')}\n"
            f"Город: {data.get('birth_city')}"
        )
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
        )
        await message.answer(text, reply_markup=keyboard)
