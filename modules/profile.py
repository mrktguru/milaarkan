from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db import save_user, get_user

class ProfileForm(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_city = State()

def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_profile")
    async def profile_menu(callback: types.CallbackQuery):
        user = await get_user(callback.from_user.id)
        if user:
            text = (
                f"🧘 Твой профиль:\n\n"
                f"Имя: {user[2]}\n"
                f"Дата рождения: {user[3]}\n"
                f"Время рождения: {user[4]}\n"
                f"Город рождения: {user[5]}"
            )
        else:
            text = "🧘 Профиль пуст. Хочешь заполнить?"

        keyboard = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("✏️ Заполнить/Изменить", callback_data="profile_edit"),
            InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
        )
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "profile_edit")
    async def start_profile_edit(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.edit_text("Как тебя зовут?")
        await ProfileForm.name.set()
        await state.update_data(telegram_id=callback.from_user.id)
        await callback.answer()

    @dp.message_handler(state=ProfileForm.name)
    async def fsm_name(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer("Укажи дату рождения (например, 01.01.2000):")
        await ProfileForm.next()

    @dp.message_handler(state=ProfileForm.birth_date)
    async def fsm_birth_date(message: types.Message, state: FSMContext):
        await state.update_data(birth_date=message.text)
        await message.answer("Укажи время рождения (например, 14:30 или 'не знаю'):")
        await ProfileForm.next()

    @dp.message_handler(state=ProfileForm.birth_time)
    async def fsm_birth_time(message: types.Message, state: FSMContext):
        await state.update_data(birth_time=message.text)
        await message.answer("Укажи город рождения:")
        await ProfileForm.next()

    @dp.message_handler(state=ProfileForm.birth_city)
    async def fsm_birth_city(message: types.Message, state: FSMContext):
        data = await state.get_data()
        await save_user(
            telegram_id=data["telegram_id"],
            name=data["name"],
            birth_date=data["birth_date"],
            birth_time=data["birth_time"],
            birth_city=message.text
        )
    await state.finish()
    await message.answer("✨ Спасибо! Профиль сохранён.")

# Получаем сохранённые данные и показываем профиль
user = await get_user(message.from_user.id)
text = (
    f"🧘 Твой профиль:\n\n"
    f"Имя: {user[2]}\n"
    f"Дата рождения: {user[3]}\n"
    f"Время рождения: {user[4]}\n"
    f"Город рождения: {user[5]}"
)

keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("✏️ Изменить профиль", callback_data="profile_edit"),
    InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
)

await message.answer(text, reply_markup=keyboard)

