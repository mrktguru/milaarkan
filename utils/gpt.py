import os
import random
from datetime import datetime, timedelta
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

# ========== Гороскоп на день ==========

async def generate_horoscope_for_sign(
    sign: str,
    period: str = "auto",
    personal: bool = False,
    name: str = None
) -> list[str]:
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(tz)

    if period == "auto":
        day_text = "завтра" if now.hour >= 20 else "сегодня"
        length_hint = "Сделай текст не длиннее 700 символов, но глубоким и ёмким."
    else:
        day_text = period
        length_hint = ""

    model = "gpt-4-turbo" if personal else "gpt-3.5-turbo"
    salutation = f"для человека по имени {name}" if personal and name else f"для знака {sign}"
    creative_hint = random.choice(CREATIVE_STYLES)
    tension_hint = (
        random.choice([
            "Добавь предчувствие, что день может быть напряжённым.",
            "Пусть будет лёгкое внутреннее напряжение — но не пугай.",
            "Пусть день звучит как вызов, но с возможностью роста.",
        ]) if random.random() < 0.2 else ""
    )

    prompt = (
        "Ты — Мила Аркан. Астролог и практикующий психолог с 10-летним опытом.\n"
        "Ты не утешаешь, не уговариваешь — ты тонко наблюдаешь и чувствуешь.\n"
        "Ты не подписываешься 'с любовью' и не используешь обращения типа 'моя дорогая'.\n\n"
        f"Напиши гороскоп {salutation} на {day_text}.\n"
        f"{length_hint}\n"
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


# ========== Гороскоп на неделю ==========

def format_week_dates():
    tz = pytz.timezone("Europe/Moscow")
    base_date = datetime.now(tz) + timedelta(days=1)
    formatted = []
    for i in range(7):
        d = base_date + timedelta(days=i)
        day = d.strftime("%d")
        month = d.strftime("%B").lower()
        weekday = d.strftime("%A")
        date_string = f"{day} {get_russian_month(month)}, {get_russian_weekday(weekday)}"
        formatted.append(date_string)
    return formatted

def get_russian_month(month):
    mapping = {
        "january": "января", "february": "февраля", "march": "марта",
        "april": "апреля", "may": "мая", "june": "июня",
        "july": "июля", "august": "августа", "september": "сентября",
        "october": "октября", "november": "ноября", "december": "декабря"
    }
    return mapping.get(month.lower(), month)

def get_russian_weekday(day):
    mapping = {
        "monday": "Понедельник", "tuesday": "Вторник", "wednesday": "Среда",
        "thursday": "Четверг", "friday": "Пятница",
        "saturday": "Суббота", "sunday": "Воскресенье"
    }
    return mapping.get(day.lower(), day)

async def generate_weekly_horoscope(sign: str, personal: bool = False, name: str = None) -> list[str]:
    model = "gpt-4-turbo" if personal else "gpt-3.5-turbo"
    creative_hint = random.choice(CREATIVE_STYLES)

    salutation = f"для человека по имени {name}" if personal and name else f"для знака {sign}"

    tension_instruction = (
        "Сделай 1 или 2 дня недели немного тревожными, эмоционально сложными или чувствительными. "
        "Это может быть тонко, с внутренним напряжением, без пугания. "
        "Пусть человек почувствует — именно в эти дни стоит быть особенно внимательной к себе."
    )

    prompt = (
        "Ты — Мила Аркан. Астролог и практикующий психолог с 10-летним опытом.\n"
        "Ты говоришь без мистики, но чувствуешь энергии.\n"
        "Ты не даёшь шаблонов, не утешаешь — ты наблюдаешь и направляешь.\n\n"
        f"Напиши гороскоп {salutation} на 7 дней начиная с завтрашнего дня.\n"
        "Для каждого дня укажи дату в формате: 04 апреля, Суббота.\n"
        "Каждый день должен быть таким же по длине, как обычный гороскоп на день (не короткий).\n\n"
        f"{tension_instruction}\n"
        f"{creative_hint}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=2500
    )

    content = response.choices[0].message.content.strip()
    return split_text_safe(content)


# ========== Разбиение текста ==========

def split_text_safe(text: str) -> list[str]:
    paragraphs = re.split(r"\n{2,}|\n(?=\w)", text)
    if len(paragraphs) == 1:
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
    spaced_text = "\n\n".join(paragraphs).strip()
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
