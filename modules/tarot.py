from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.time_status import is_mila_online, online_status_text


def setup(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data == "menu_tarot")
    async def show_tarot_menu(callback: types.CallbackQuery):
        text = (
            "🃏 Таро-расклады\n\n"
            "Иногда, чтобы прояснить ситуацию, достаточно правильно задать вопрос внутри.\n\n"
            "Выбери расклад, который откликается тебе сейчас:"
        )
        await callback.message.edit_text(text, reply_markup=tarot_menu_keyboard())
        await callback.answer()

    @dp.callback_query_handler(lambda c: c.data.startswith("tarot_"))
    async def show_tarot_info(callback: types.CallbackQuery):
        data_key = callback.data

        status = online_status_text()

        texts = {
            "tarot_day": f"{status}\n\n🃏 Карта дня — 50 энергии\n\n"
                         "Сконцентрируйся. Один символ. Один акцент.\n"
                         "Подсказка, на чём сфокусироваться в течение дня.",

            "tarot_compass": f"{status}\n\n🌿 Внутренний компас — 100 энергии\n\n"
                             "Прошлое — Настоящее — Будущее.\n"
                             "Помогает почувствовать, где ты и куда направляется твоя энергия.",

            "tarot_love": f"{status}\n\n❤️ Отношения — 250 энергии\n\n"
                          "Ты — Он/Она — Что вас соединяет — Что мешает — Возможный вектор.",

            "tarot_action": f"{status}\n\n💼 Моя ситуация — 250 энергии\n\n"
                            "Суть запроса — влияние — скрытые импульсы — возможный результат — совет.",

            "tarot_free": f"{status}\n\n🔮 Свободный вопрос — 300 энергии\n\n"
                          "Ты задаёшь вопрос — карта отвечает образом, через который приходит подсказка."
        }

