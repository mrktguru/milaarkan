import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_horoscope_for_sign(sign: str, period: str = "сегодня") -> str:
    prompt = (
        f"Ты — Мила Аркан, астролог и практикующий психолог с 10-летним опытом.\n"
        f"Напиши гороскоп для знака {sign} на {period}.\n\n"
        "Пиши от первого лица, как будто ты обращаешься к женщине, которая ищет поддержку и ясность. "
        "Стиль — тёплый, уважительный, с лёгким прикосновением интуиции. "
        "Не используй общие фразы, сделай текст живым, как будто ты говоришь лично ей."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=400
    )

    return response.choices[0].message.content.strip()
