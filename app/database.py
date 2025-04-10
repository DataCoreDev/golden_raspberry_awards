import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Caminhdo do arquivo do banco de dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "databd", "gra_app.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

#Gerando a conexão com o BD
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

#Iniciando a sessão
Session_Local = sessionmaker(bind=engine)
Base = declarative_base()

