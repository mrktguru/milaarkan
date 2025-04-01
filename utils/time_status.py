from datetime import datetime, timedelta
import pytz

def is_mila_online():
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(tz)

    start_hour = 9
    end_hour = 4

    if now.hour >= start_hour or now.hour < end_hour:
        return True
    return False

def online_status_text():
    return "🟢 Мила в сети" if is_mila_online() else "🔘 Мила не в сети"
