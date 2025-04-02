import os
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_LENGTH = 3500  # безопасная длина одного сообщения Telegram

# Возможные творческие акценты для вариативности
CREATIVE_STYLES = [
    "Пусть тон будет как письмо старшей подруге.",
    "Используй метафору воды, ветра или света.",
    "Добавь фразу, которая звучит как внутреннее вдохновение.",
    "В конце — мягкий психологический совет.",
    "Представь, что ты пишешь человеку, который не верит в гороскопы — но ищет знак.",
]

async def generate_horoscope_for_sign(
    sign: str,
    period: str = "сегодня",
    personal: bool = False,
    name: str = None
) -> list[str]:
    # Выбираем модель в зависимости от контекста
    model = "gpt-4-turbo" if personal else "gpt-3.5-turbo"

    # Добавляем творческую вариативность
    creative_hint = random.choice(CREATIVE_STYLES)

    # Формируем обращение
    if personal and name:
        salutation = f"для человека по имени {name}"
    else:
        salutation = f"для знака {sign}"

    # Формируем промт
    prompt = (
        f"Ты — Мила Аркан, астролог и практикующий психолог с 10-летним опытом.\n"
        f"Напиши гороскоп {salutation} на {period}.\n\n"
        "Пиши от первого лица, как будто ты лично обращаешься к читателю. "
        "Стиль — тёплый, психологичный, уважительный. Избегай шаблонов и общих фраз. "
        "Говори глубоко, интуитивно, но ясно. "
        f"{creative_hint}"
    )

    # Отправляем запрос
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.95,  # больше разнообразия
        max_tokens=1000
    )

    content = response.choices[0].message.content.strip()
    return split_text_safe(content)


def split_text_safe(text: str) -> list[str]:
    chunks = []
    while text:
        if len(text) <= MAX_LENGTH:
            chunks.append(text)
            break
        split_pos = text.rfind("\n", 0, MAX_LENGTH)
        if split_pos == -1:
            split_pos = MAX_LENGTH
        chunks.append(text[:split_pos].strip())
        text = text[split_pos:].strip()
    return chunks
