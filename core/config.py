# Единая точка входа для всех настроек проекта 
# Загружает переменные окружения из .env и передает их в кол

import os
from dotenv import load_dotenv

# Загрузить переменные из .env в os.environ
load_dotenv()

# Просто читаем нужные переменные
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Проверим, что ничего не забыли
if not BOT_TOKEN:
    raise ValueError("Переменная BOT_TOKEN не найдена в .env")

if not DATABASE_URL:
    raise ValueError("Переменная DATABASE_URL не найдена в .env")

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
