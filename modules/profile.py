from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_profile")
    async def profile_menu(callback: types.CallbackQuery):
        text = (
            "🧘 Профиль пользователя\n\n"
            "Здесь ты можешь указать или изменить данные для персональных гороскопов:\n"
            "• Имя\n"
            "• Дата и время рождения\n"
            "• Город рождения\n\n"
            "Эти данные помогают мне точнее составить карту твоей души."
        )
        await callback.message.edit_text(text, reply_markup=profile_menu_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data == "profile_edit")
    async def profile_edit_placeholder(callback: types.CallbackQuery):
        text = (
            "✏️ В будущем здесь будет форма редактирования профиля.\n\n"
            "Пока ты можешь отправить мне свои данные вручную."
        )
        await callback.message.edit_text(text, reply_markup=profile_menu_keyboard())
        await callback.answer()

def profile_menu_keyboard():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("✏️ Изменить профиль", callback_data="profile_edit"),
        InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
    )
