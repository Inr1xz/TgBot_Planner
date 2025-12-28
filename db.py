# create_engine - создает подключение к базе данных
# Соlumn - используется для описания полей в таблице 
# Integer, String, DataTime - типы данных полей 
from sqlalchemy import create_engine, Column, Integer, String, DateTime
# declaretive_base - базовый класс от которого будут наследоваться все таблицы
# sessionmaker - создает фабрику сессий для взаимодействия с базой (добавление, удаление, запросы)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from core.config import DATABASE_URL
from sqlalchemy import Boolean

# Создаем базовый класс, от которого будут наследоваться все модели таблиц
Base = declarative_base()

# Создаем модель таблицы Task - он будет соответствовать таблице tasks в базе 
class Task(Base):
    # Указываем имя таблицы в базе данных
    __tablename__ = "tasks"
    # Поле id: Integet - тип данных, primary_key=True - деляет это поле уникальным индетефикатором записи
    id = Column(Integer, primary_key=True)
    # Поле user_id: хранит идентификатор пользователя Telegram
    user_id = Column(Integer, nullable=False)
    # Поле description: текстовое описсание задачи, nullable=False - обязательное значение
    description = Column(String, nullable=False)
    # Поле done: булевое значение отслеживает выполнено ли или нет
    is_done = Column(Boolean, default=False)



# Cоздем движок подключения к SQLite - база будет хранится в planner.db
engine = create_engine(DATABASE_URL)
# Создаем фабрику сессий для взаимодейтсвия с базой через созданный движок
Session = sessionmaker(bind=engine)
# Создает все таблицы в базе, описанные через Base. Если planner.db не существует он будет создан
Base.metadata.create_all(bind=engine)

# Добавляет новую задачу от пользователя в БД
def add_task(user_id: int, description: str):
    # Создаем сессию подключения к БД
    session = Session()
    # Создаем объект задачи
    task = Task(user_id=user_id, description=description)
    # Добавляем задачу в БД
    session.add(task)
    # Сохраняем изменения 
    session.commit()
    # Закрываем сессию
    session.close()

# Возвращаем все задачи конкретного пользователя
def get_tasks(user_id: int):
    session = Session()
    # Ищем задачу по ID
    tasks = session.query(Task).filter_by(user_id=user_id).all()
    session.close()
    # Возвращаем список задач
    return tasks

# Помечаем задачу как выполненную по ID
def mark_task_done(task_id: int):
    session = Session()
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        # Помечаем задачу как выполненную
        task.is_done = True 
        session.commit()
    session.close()

# Удаляем задачу из списка
def delete_task(user_id, task_id):
    session = Session()
    task = session.query(Task).filter_by(id=task_id, user_id=user_id).first()
    if task:
        session.delete(task)
        session.commit()
        result = True
    else:
        result = False
    session.close()
    return result