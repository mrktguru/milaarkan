from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules.main_menu import show_main_menu


def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_about")
    async def about_menu(callback: types.CallbackQuery):
        text = (
            "📖 Обо мне\n\n"
            "Я — Мила Аркан, астролог и практикующий психолог.\n"
            "Более 10 лет я помогаю людям находить опору внутри себя через\n"
            "язык звёзд, архетипов и символов.\n\n"
            "Мой подход — бережный, интуитивный и всегда немного магический.\n"
            "Если ты здесь — возможно, это знак.\n"
        )
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
        )
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
    @dp.callback_query_handler(lambda c: c.data == "main_menu")
    async def back_to_main(callback: types.CallbackQuery):
        await show_main_menu(callback)
