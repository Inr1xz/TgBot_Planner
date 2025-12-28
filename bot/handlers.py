from bot.api import send_message
from db import add_task, get_tasks, mark_task_done, delete_task, edit_task


def handle_message(update: dict):
    # Обрабатываем одно обновление (сообщение от пользователя)

    message = update.get("message")
    if not message:
        return
    
    # Получаем:
    # chat_id — ID чата (кому писать)
    # text — текст сообщения пользователя
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    # Если пользователь прислал /start, бот говорит "Привет!"
    if text == "/start":
        send_message(chat_id, "Привет! Я бот-планировщик. Напиши /add, /list, /done <id>.")

    elif text.startswith("/add"):
        # Удаляем команду /add и пробелы - получаем текст задачи
        task_text = text[4:].strip()
        if not task_text:
            send_message(chat_id, "Укажи описание задачи после /add.")
        else:
            add_task(chat_id, task_text)
            send_message(chat_id, "Задача добавлена.")

    elif text == "/list":
        # Получаем все задачи пользователя
        tasks = get_tasks(chat_id)
        if not tasks:
            send_message(chat_id, "У тебя нет задач.")
        else:
            # t.id - числовой индефикатор задачи
            # t.discription - текст задачи
            # t.is_dine - булевое значение выполнена задача или нет
            # Отправляем пользователю собранный список задач '\n.join' объединяет все строки в один многострочный текст раздляя симполом переноса
            reply = "\n".join(
                f"{t.id}. {'Готово: ' if t.is_done else 'Не готово: '} {t.description}" for t in tasks
            )
            send_message(chat_id, reply)

    elif text.startswith("/done"):
        try:
            # Берем число после команды 
            task_id = int(text.split()[1])
            # Отмечаем задачу как выполненную
            mark_task_done(task_id)
            send_message(chat_id, "Задача отмечена как выполненная.")
        except(IndexError, ValueError):
            send_message(chat_id, "Укажи ID задачи")

    elif text.startswith("/delete"):
        # Разделяем текст про пробелу [0] - команда /delete [1] - ID задачи
        parts = text.split(maxsplit=1)
        # Провеляем что есть вторая часть и что она состоит из цифры
        if len(parts) == 2 and parts[1].isdigit():
            # Преобразуем ID из строки в инт
            task_id = int(parts[1])
            success = delete_task(chat_id, task_id)
            if success:
                send_message(chat_id, f"Задача #{task_id} удалена")
            else:
                send_message(chat_id, f"Задача #{task_id} не найдена")
        else:
            send_message(chat_id, "Используйте формат: /delete <id>")

    elif text.startswith("/edit"):
        # Разделяем текст по пробелам на /edit, ID, Описание
        parts = text.split(maxsplit=2)
        # Проверяем что есть все три части и проверяем что вторая это цифра
        if len(parts) == 3 and parts[1].isdigit():
            task_id = int(parts[1])
            # Добавляем новое описание
            new_description = parts[2]
            success = edit_task(chat_id, task_id, new_description)
            if success:
                send_message(chat_id, f"Задача #{task_id} обновлена")
            else:
                send_message(chat_id, f"Задача #{task_id} не найдена")
        else:
            send_message(chat_id, "Используйте формат: /edit <id> <новый текст задачи>")
    
    elif text == "/help":
        # Описание всех доступных команд
        help_text = (
            "Команды:\n"

        )
        send_message(chat_id, help_text)


    # Во всех остальных случаях отправляем пользователю его же сообщение
    else:
        send_message(chat_id, f"Ты написал:  {text}")