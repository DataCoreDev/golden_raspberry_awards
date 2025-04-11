from fastapi.testclient import TestClient
from main import app
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from app.crud import import_movie_list


client = TestClient(app)

def setup_module(module):    
    # Cria as tabelas no banco em memória
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        # Importa o CSV antes do teste
        import_movie_list("databd/movielist(2).csv", db)  # usa print como logger só pra passar
    except Exception as e:
        print(f"Erro na importação do CSV durante setup do teste: {str(e)}")
    finally:
        db.close()

def test_report_intervals():
    try:
        # Testando o endpoint
        response = client.get("/producers/intervals")

        # Verificando se deu certo
        assert response.status_code == 200

        # Pegando a resposta em JSON
        data = response.json()

        # Verificando se tem os valores de min e max
        assert "min" in data
        assert "max" in data

        # Verificando se o JSON  está na estrura certa
        for item in data["min"]:
            assert "producer" in item
            assert "interval" in item
            assert "previousWin" in item
            assert "followingWin" in item

        # Verificando se o JSON  está na estrura certa
        for item in data["max"]:
            assert "producer" in item
            assert "interval" in item
            assert "previousWin" in item
            assert "followingWin" in item

        print(f"Teste realizado com sucesso!")        
    except Exception as e:
        print(f"Erro no teste. Erro: {str(e)}")        
        assert False, f"Erro no teste. Erro: {str(e)}"

