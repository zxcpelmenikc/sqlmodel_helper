from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv
from app.models import *
load_dotenv() # Загружаем переменные окружения из .env
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

def get_engine():
    return engine


def init_db():
    print(DATABASE_URL)
    SQLModel.metadata.create_all(engine)
init_db()

def close_db():
    engine.dispose()