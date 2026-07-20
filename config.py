import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if BOT_TOKEN is None:
    raise ValueError(
        "Токен бота не найден!\n"
        "1. Создайте файл .env в папке проекта\n"
        "2. Добавьте строку: BOT_TOKEN=ваш_токен_сюда\n"
        "3. Получите токен у @BotFather в Telegram"
    )