# main.py
import httpx
import time
import os
from dotenv import load_dotenv

# Загружаем токен из .env и форматируем базовый URL, к которому будем обращаться 
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Нужно, чтобы не обрабатывать ожно и то же сообщение повторно, читаем только новые, двигая offset вперед
offset = 0  

# Делаем get-запрос к Telegram API 
def get_updates():
    global offset
    response = httpx.get(f"{API_URL}/getUpdates", params={"timeout": 30, "offset": offset})
    result = response.json()
    if result["ok"]:
        return result["result"]
    return []

# Отправляем сообщение пользователю
def send_message(chat_id, text):
    httpx.post(f"{API_URL}/sendMessage", data={"chat_id": chat_id, "text": text})

# Бесконченый цикл бота 
def main():
    print("Бот запущен...")
    while True:
        updates = get_updates()
        for update in updates:
            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            if text == "/start":
                send_message(chat_id, "Привет!")
            else:
                send_message(chat_id, f"Ты написал: {text}")

            # Обновляем offset, чтобы не получать одно и то же сообщение снова
            global offset
            offset = update["update_id"] + 1

        time.sleep(1)


if __name__ == "__main__":
    main()


