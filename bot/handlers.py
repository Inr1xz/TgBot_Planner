from bot.api import send_messsage

def handle_message(update: dict):
    # Обрабатываем одно обновление (сообщение от пользователя)

    message = update.get("message")
    if not message:
        return
    
    # Получаем:
    # chat_id — ID чата (кому писать)
    # text — текст сообщения пользователя
    chat_id = message["chat_id"]["id"]
    text = message.get("text", "")

    # Если пользователь прислал /start, бот говорит "Привет!" иначе — отражает сообщение
    if text == "/start":
        send_messsage(chat_id, "Привет! Я бот-планировщик. Напиши задачу или используй команду.")
    else:
        send_messsage(chat_id, f"Ты написал: {text}")