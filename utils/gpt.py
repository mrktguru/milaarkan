import os
import random
from datetime import datetime
import pytz
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_LENGTH = 3500

CREATIVE_STYLES = [
    "Пусть тон будет как письмо старшей подруге.",
    "Используй метафору воды, ветра или света.",
    "Добавь фразу, которая звучит как внутреннее вдохновение.",
    "В конце — мягкий психологический совет.",
    "Представь, что ты пишешь человеку, который не верит в гороскопы — но ищет знак.",
]

TENSION_STYLES = [
    "Сделай акцент на том, что день может быть эмоционально сложным.",
    "Добавь тонкое предупреждение — как будто что-то внутри подсказывает быть осторожнее.",
    "Позволь себе чуть больше тревоги в словах, но не теряя уважительного тона.",
    "Пусть гороскоп звучит как внутреннее предчувствие — что не всё будет легко.",
    "Намекни, что энергия дня требует внимательности и осторожности.",
]


def get_current_period_text() -> tuple[str, str]:
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(tz)
    if now.hour >= 20:
        return "завтра", "Сделай его немного короче — лаконично, но с глубиной (до 500 символов)"
    return "сегодня", "Сделай гороскоп лаконичным — не длиннее 700 символов, но ёмко и осмысленно"


async def generate_horoscope_for_sign(
    sign: str,
    period: str = "auto",
    personal: bool = False,
    name: str = None
) -> list[str]:
    if period == "auto":
        day_text, length_hint = get_current_period_text()
    else:
        day_text = period
        length_hint = ""

    model = "gpt-4-turbo" if personal else "gpt-3.5-turbo"
    creative_hint = random.choice(CREATIVE_STYLES)
    tension_hint = random.choice(TENSION_STYLES) if random.random() < 0.2 else ""

    salutation = f"для человека по имени {name}" if personal and name else f"для знака {sign}"

    prompt = (
        f"Ты — Мила Аркан, астролог и практикующий психолог с 10-летним опытом.\n"
        f"Напиши гороскоп {salutation} на {day_text}.\n\n"
        f"{length_hint}\n"
        "Пиши от первого лица, избегай шаблонов. Стиль — тёплый, психологичный, интуитивный и уважительный.\n"
        f"{creative_hint}\n"
        f"{tension_hint}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.95,
        max_tokens=1000
    )

    content = response.choices[0].message.content.strip()
    return split_text_safe(content)


def split_text_safe(text: str) -> list[str]:
    # Попробуем разбить по существующим абзацам
    paragraphs = re.split(r"\n{2,}|\n(?=\w)", text)
    if len(paragraphs) == 1:
        # Принудительно разобьём по предложениям
        sentences = re.split(r'(?<=[.!?]) +', text)
        paragraphs = []
        chunk = ""
        for i, sentence in enumerate(sentences, 1):
            chunk += sentence.strip() + " "
            if i % 2 == 0:
                paragraphs.append(chunk.strip())
                chunk = ""
        if chunk:
            paragraphs.append(chunk.strip())

    # Склеиваем с разрежённостью
    spaced_text = "\n\n".join(paragraphs).strip()

    # Разбиваем по длине Telegram
    chunks = []
    while spaced_text:
        if len(spaced_text) <= MAX_LENGTH:
            chunks.append(spaced_text)
            break
        split_pos = spaced_text.rfind("\n\n", 0, MAX_LENGTH)
        if split_pos == -1:
            split_pos = MAX_LENGTH
        chunks.append(spaced_text[:split_pos].strip())
        spaced_text = spaced_text[split_pos:].strip()
    return chunks
