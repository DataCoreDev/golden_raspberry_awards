from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Caminhdo do arquivo do banco de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/gra_app.db"

#Gerando a conexão com o BD
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

#Iniciando a sessão
Sessionlocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

