# create_engine - создает подключение к базе данных
# Соlumn - используется для описания полей в таблице 
# Integer, String, DataTime - типы данных полей 
from sqlalchemy import create_engine, Column, Integer, String, DateTime
# declaretive_base - базовый класс от которого будут наследоваться все таблицы
# sessionmaker - создает фабрику сессий для взаимодействия с базой (добавление, удаление, запросы)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Cоздем движок подключения к SQLite - база будет хранится в planner.db
# echo = True - логирует все SQL - запросы в консоль
engine = create_engine("sqlite://planner.db", echo=True)
# Создаем фабрику сессий для взаимодейтсвия с базой через созданный движок
SessionLocal = sessionmaker(bind=engine)
# Создаем базовый класс, от которого будут наследоваться все модели таблиц
Base = declarative_base()

# Создаем модель таблицы Task - он будет соответствовать таблице tasks в базе 
class Task(Base):
    # Указываем имя таблицы в базе данных
    __tablename__ = "tasks"
    # Поле id: Integet - тип данных, primary_key=True - деляет это поле уникальным индетефикатором записи, index=True - создает индекс, ускоряющий поиск по этому полю
    id = Column(Integer, primary_key=True, index=True)
    # Поле user_id: хранит идентификатор пользователя Telegram, index=True - также индексируется для быстрого поиска
    user_id = Column(Integer, index=True)
    # Поле description: текстовое описсание задачи, nullable=False - обязательное значение
    descriprion = Column(String, nullable=False)
    # Хранит дату и время выполнения задачи
    due_date = Column(DateTime, default=datetime.utcnow)

# Функция инициализации базы данных
def init_db():
# Создает все таблицы в базе, описанные через Base. Если planner.db не существует он будет создан
    Base.metadata.create_all(bind=engine)

