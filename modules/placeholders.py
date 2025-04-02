from aiogram import types
from aiogram.dispatcher import Dispatcher

def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_question")
    async def question_placeholder(callback: types.CallbackQuery):
        await callback.answer("Этот раздел скоро появится ✨", show_alert=True)

    @dp.callback_query_handler(lambda c: c.data in ["pay_100", "pay_300", "pay_1000"])
    async def payment_placeholder(callback: types.CallbackQuery):
        await callback.answer("Оплата пока не подключена. Но ты можешь пополнить энергию позже 💎", show_alert=True)
