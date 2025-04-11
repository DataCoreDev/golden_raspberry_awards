import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Caminhdo do arquivo do banco de dados físico
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#DB_PATH = os.path.join(BASE_DIR, "databd", "gra_app.db")
#SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

#Banco de dados em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///file:memdb1?mode=memory&cache=shared&uri=true"

# Cria o engine e **mantém ele vivo**
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,    
)

# Sessão fixa, ligada ao engine acima
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

