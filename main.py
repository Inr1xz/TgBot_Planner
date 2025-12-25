import time
from bot.api import get_updates, send_messsage

# Нужно, чтобы не обрабатывать ожно и то же сообщение повторно, читаем только новые, двигая offset вперед
offset = 0  

# Бесконченый цикл бота 
def main():
    print("Бот запущен...")
    # Объявляем offset глобальным, потому что мы будем его изменять внутри функции
    global offset

    while True:
        # Получаем список обновлений из Telegram API
        updates = get_updates(offset)
        # Извлекаем текстовое сообщение.
        for update in updates:
            message = update.get("message")
            if not message:
                continue

            # Получаем:
            # chat_id — ID чата (кому писать)
            # text — текст сообщения пользователя
            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            #если пользователь прислал /start, бот говорит "Привет!" иначе — отражает сообщение
            if text == "/start":
                send_messsage(chat_id, "Привет")
            else:
                send_messsage(chat_id, f"Ты написал: {text}")

            #Telegram присваивает каждому обновлению update_id. Мы прибавляем +1, чтобы не получать это обновление снова
            offset = update["update_id"] + 1 
        
        time.sleep(1)


if __name__ == "__main__":
    main()


