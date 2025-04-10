from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import app.models, app.crud, app.utils
from app.database import Session_Local, engine, Base
from app.schemas import Interval_Response
from app.utils import import_movie_list

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = Session_Local()

    try:
        yield db
    finally:
        db.close()

#Endereço para o endpoint de importar o arquivo CSV
@app.post("/producers/import")
def import_CSV(db: Session = Depends(get_db)):
    try:
        # Def feita no app/utils
        import_movie_list("databd/movielist(2).csv", db)

        # Retornando uma mensagem de sucesso
        return {
            "message": "Arquivo importado com sucesso!",
            "file": "movies.csv"
        }        
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.message)

#Endereço do endpoint de intervalos, junto da def
@app.get("/producers/intervals", response_model=Interval_Response)
def get_Intervals(db : Session = Depends(get_db)):
    return None
