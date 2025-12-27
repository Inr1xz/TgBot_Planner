from api import send_messsage
from db import add_task, get_tasks, mark_task_done

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

    # Если пользователь прислал /start, бот говорит "Привет!"
    if text == "/start":
        send_messsage(chat_id, "Привет! Я бот-планировщик. Напиши /add, /list, /done <id>.")
    elif text.startswitch("/add"):
        # Удаляем команду /add и пробелы - получаем текст задачи
        task_text = text[4:].strip()
        if not task_text:
            send_messsage(chat_id, "Укажи описание задачи после /add.")
        else:
            add_task(chat_id, task_text)
            send_messsage(chat_id, "Задача добавлена.")
    elif text == "/list":
        # Получаем все задачи пользователя
        tasks == get_tasks(chat_id)
        if not tasks:
            send_messsage(chat_id, "У тебя нет задач.")
        else:
            # t.id - числовой индефикатор задачи
            # t.discription - текст задачи
            # t.is_dine - булевое значение выполнена задача или нет
            # Отправляем пользователю собранный список задач '\n.join' объединяет все строки в один многострочный текст раздляя симполом переноса
            reply = "\n".join(
                f"{t.id}. {'Готово: ' if t.is_done else 'Не готово: '} {t.description}" for t in tasks
            )
            send_messsage(chat_id, reply)
    elif text.startswitch("/done"):
        try:
            # Берем число после команды 
            task_id = int(text.split()[1])
            # Отмечаем задачу как выполненную
            mark_task_done(task_id)
            send_messsage(chat_id, "Задача отмечена как выполненная.")
        except(IndexError, ValueError):
            send_messsage(chat_id, "Укажи ID задачи")
    # Во всех остальных случаях отправляем пользователю его же сообщение
    else:
        send_messsage(chat_id, f"Ты написал:  {text}")