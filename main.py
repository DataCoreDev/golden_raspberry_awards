import os
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal, engine, Base
from app.schemas import Interval_Response
from datetime import datetime
from app.crud import report_intervals, import_movie_list

app = FastAPI()

today = datetime.now().date()

# Variáveis para o arquivo de log
LOG_DIR = 'logs'
NOME_ARQUIVO_LOG = f'{LOG_DIR}\\gra_{str(today.day).zfill(2)}-{str(today.month).zfill(2)}-{str(today.year).zfill(4)}.log'

# Criação do diretório de logs, caso não exista
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configuração de logging
logging.basicConfig(filename=NOME_ARQUIVO_LOG, level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

def get_db():
    logging.info(f'Conectando com o BD...')
    db = SessionLocal()

    try:
        yield db        
    finally:
        logging.info(f'Conexão realizada com o BD...')
        db.close()

# Garante que tudo está pronto ao iniciar

@app.on_event("startup")
def on_startup():
    logging.info("Criando tabelas...")
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        logging.error(f"Erro ao criar tabelas: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao criar tabelas no banco de dados.")
    
    logging.info("Importando CSV inicial...")
    db = SessionLocal()
    try:
        import_movie_list("databd/movielist(2).csv", db, logging)
        logging.info("CSV importado com sucesso.")
    except Exception as e:
        logging.error(f"Erro na importação inicial: {str(e)}")
    finally:
        db.close()


# Endereço para o endpoint de importar o arquivo CSV
'''
Removido pois a importação vai acontecer no iniciar da app

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
'''

# Endereço do endpoint de intervalos, junto da def
@app.get("/producers/intervals", response_model=Interval_Response)
def get_Intervals(db : Session = Depends(get_db)):
    try:
        # Registrando no log
        logging.info(f'Iniciando relatório de intervalo...')        
        
        return report_intervals(db, logging)        

    except Exception as e:
        logging.error(f'Erro na importação. Erro: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))
