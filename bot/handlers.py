from bot.api import send_message
from db import add_task, get_tasks, mark_task_done, delete_task, edit_task
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from datetime import datetime, timedelta


add_steps = {}

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

    if chat_id in add_steps:
        step = add_steps[chat_id]["step"]

        if step == "desc":
            add_steps[chat_id]["desc"] = text
            add_steps[chat_id]["step"] = "priority"
            send_message(chat_id, "Укажи приоритет (1-5):")
            
        elif step == "priority":
            if text.isdigit() and 1 <= int(text) <= 5:
                add_steps[chat_id]["priority"] = int(text)
                add_steps[chat_id]["step"] = "date"
                send_message(chat_id, "Укажи дату в формате ГГГГ-ММ-ДД")
            else:
                send_message(chat_id, "Приоритет должен быть числом от 1 до 5")
            
        elif step == "date":
            try:
                date = datetime.strptime(text, "%Y-%m-%d").date()
                add_steps[chat_id]["date"] = date
                add_steps[chat_id]["step"] = "time"
                send_message(chat_id, "Укажи время в формате ЧЧ:ММ:")
            except ValueError:
                send_message(chat_id, "Неверный формат. Введите дату как ГГГГ-ММ-ДД")

        elif step == "time":
            try:
                time = datetime.strptime(text, "%H:%M").time()
                data = add_steps.pop(chat_id)
                due_datetime = datetime.combine(data["date"], time)
                add_task(chat_id, data["desc"], data["priority"], due_datetime)
                send_message(chat_id, f"Задача добавлена на {due_datetime.strftime('%Y-%m-%d %H:%M')}")
            except ValueError:
                send_message(chat_id, "Неверный формат. Введи время как ЧЧ:ММ")
        return


    # Если пользователь прислал /start, бот говорит "Привет!"
    if text == "/start":
        send_message(chat_id, "Привет! Я бот-планировщик")

    elif text.startswith("/add"):
        add_steps[chat_id] = {"step": "desc"}
        send_message(chat_id, "Введите описание задачи:")


    elif text == "/list":
        # Получаем все задачи пользователя
        tasks = get_tasks(chat_id)
        if not tasks:
            send_message(chat_id, "У тебя нет задач.")
        else:
            msg_lines = []
            for task in tasks:
                status = "Выполнено" if task.is_done else "Не выполнено"
                due = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "Без даты"
                msg_lines.append(f"{task.id}. {status} [{task.priority}] {task.description} ({due})")
            send_message(chat_id, "\n".join(msg_lines))

    elif text.startswith("/done"):
        parts = text.split(maxsplit=1)
        if len(parts) == 2 and parts[1].isdigit():
            task_id = int(parts[1])
            success = mark_task_done(chat_id, task_id)
            if success:
                send_message(chat_id, f"Задача #{task_id} отмечена как выполненная")
            else:
                send_message(chat_id, f"Задача #{task_id} не найдена")
        else:
            send_message(chat_id, "Используйте формат: /done <id>")


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

    # Во всех остальных случаях отправляем пользователю
    else:
        send_message(chat_id, "Неизвестная команда. Напищите /help для списка команд.")

