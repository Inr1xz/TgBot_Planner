# Единая точка входа для всех настроек проекта 
# Загружает переменные окружения из .env и передает их в кол

from pydantic import BaseSettings 
from dotenv import load_dotenv 

# Загружаем переменные окружения из .env 
load_dotenv()

# Описываем нужные переменные
class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str 

# Указываем откуда брать переменные, чтобы это работало в любой среде
    class Config:
        env_file = ".env"
        env_file_encording = "utf-8"

# Создаем объект из которого будем брать
settings = Settings()

