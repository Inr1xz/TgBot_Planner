import httpx 
from core.config import API_URL 

# Делаем get-запрос к Telegram API, чтобы получить новые сообщения от пользователей
def get_updates(offset):
    # Делаем GET-запрос с параметрами: 
    # offset — чтобы не получать старые сообщения
    # timeout=30 — long-polling: сервер Telegram будет "висеть" до 30 сек, пока не придёт новое сообщение
    response = httpx.get(f"API_URL/getUpdates", params = {"timeout": 30, "offset": offset})
    # Получаем JSON-ответ и преобразуем в Python-словарь
    result = response.json()
    if result["ok"]:
        return result["result"]
    return[]

# Отправляем сообщение пользователю
def send_message(chat_id, text):
    # POST-запрос на метод /sendMessage Telegram API. Параметры:
    # chat_id — куда отправлять
    # text — что отправлять
    httpx.post(f"{API_URL}/sendMessage", data = {"chat_id": chat_id, "text": text})
