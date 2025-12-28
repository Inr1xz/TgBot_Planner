import httpx 
from core.config import API_URL 

# Делаем get-запрос к Telegram API, чтобы получить новые сообщения от пользователей
def get_updates(offset):
    # Делаем GET-запрос с параметрами: 
    # offset — чтобы не получать старые сообщения
    response = httpx.get(f"{API_URL}/getUpdates", params={"offset": offset}, trust_env=False)
    # Получаем JSON-ответ и преобразуем в Python-словарь
    result = response.json()
    if result["ok"]:
        return result["result"]
    return[]

# Отправляем сообщение пользователю
def send_message(chat_id, text, reply_markup=None):
    # POST-запрос на метод /sendMessage Telegram API. Параметры:
    # chat_id — куда отправлять
    # text — что отправлять
    httpx.post(f"{API_URL}/sendMessage", data = {"chat_id": chat_id, "text": text}, trust_env=False)
