import os
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import app.models, app.crud, app.utils
from app.database import Session_Local, engine, Base
from app.schemas import Interval_Response
from app.utils import import_movie_list
from datetime import datetime

app = FastAPI()

Base.metadata.create_all(bind=engine)

today = datetime.now().date()

# Variáveis para o arquivo de log
LOG_DIR = 'logs'
NOME_ARQUIVO_LOG = f'{LOG_DIR}\\robo_calibracoes_{str(today.day).zfill(2)}\
    -{str(today.month).zfill(2)}-{str(today.year).zfill(4)}.log'

# Criação do diretório de logs, caso não exista
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configuração de logging
logging.basicConfig(filename=NOME_ARQUIVO_LOG, level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

def get_db():

    logging.info(f'Conectando com o BD...')
    db = Session_Local()

    try:
        yield db        
    finally:
        logging.info(f'Conexão realizada com o BD...')
        db.close()

# Endereço para o endpoint de importar o arquivo CSV
@app.post("/producers/import")
def import_CSV(db: Session = Depends(get_db)):
    try:
        # Registrando no log
        logging.info(f'Iniciando importação...')

        # Def feita no app/utils
        import_movie_list("databd/movielist(2).csv", db, logging)

        logging.info(f'Importação realizada...')

        # Retornando uma mensagem de sucesso
        return {
            "message": "Arquivo importado com sucesso!",
            "file": "movielist(2).csv"
        }        
    except Exception as e:
        logging.error(f'Erro na importação. Erro: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))

# Endereço do endpoint de intervalos, junto da def
@app.get("/producers/intervals", response_model=Interval_Response)
def get_Intervals(db : Session = Depends(get_db)):
    return None
