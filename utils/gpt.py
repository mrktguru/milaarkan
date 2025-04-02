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

    # Добавим инструкцию про тревожные дни
    tension_instruction = (
        "Сделай 1 или 2 дня недели немного напряжёнными или тревожными. "
        "Пусть это будет не страшно, а как будто смена фона, эмоциональная глубина. "
        "Пусть человек почувствует — именно в эти дни стоит быть особенно внимательной к себе."
    )

    date_headers = format_week_dates()
    date_block = "\n".join([f"{date} — ..." for date in date_headers])

    prompt = (
        "Ты — Мила Аркан.\n"
        "Ты астролог и практикующий психолог с 10-летним опытом. "
        "Ты говоришь без мистики, но чувствуешь энергии. "
        "Ты не даёшь шаблонов, не утешаешь — ты наблюдаешь и направляешь.\n\n"
        f"Напиши гороскоп {salutation} на 7 дней начиная с завтрашнего дня.\n"
        "Для каждого дня укажи дату в формате: 04 апреля, Суббота.\n"
        "Не сокращай — каждый день должен быть такой же по длине, как обычный гороскоп на день.\n\n"
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
