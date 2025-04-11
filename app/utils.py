import pandas as pd
from datetime import datetime
from app.models import Movie

# Função para importar o arquivo CSV e salvar no banco de dados
def import_movie_list(path, db, log):
    # Primeiro verificar se o aquivo antes de importar, se não existir retorna um erro
    try:
        log.info(f'Verificando se o arquivo existe...')
        csv_file = pd.read_csv(path, delimiter=';', quoting=3)
    except Exception as e:
        raise FileNotFoundError(f"Erro ao carregar arquivo. Erro: {e}")
    
    # Verifica se o arquivo está vazio
    log.info(f'Verificando se o arquivo está vazio...')
    if csv_file.empty:
        raise ValueError("Arquivo CSV vazio.")
    
    # Verifica se as colunas necessárias estão presentes
    log.info(f'Validando as colunas...')
    required_columns = ["year", "title", "studios", "producers", "winner"] 
    for col in required_columns:
        if col not in csv_file.columns:
            log.error(f'Coluna {col} não encontrada no arquivo CSV.')
            raise ValueError(f"Coluna {col} não encontrada no arquivo CSV.")
        
    try:
        # Converte o DataFrame para uma lista de dicionários    
        log.info(f'Convertendo o dataframe...')
        data = csv_file.to_dict(orient="records") 
        movie = None       

        # Iterando sobre os dados e criando os Movies
        log.info(f'iterando linhas...')
        for row in data:
            # Buscando no BD se o filme já existe
            movie_exists = db.query(Movie).filter_by(
                year=row["year"],
                title=row["title"],
                studios=row["studios"],
                producers=row["producers"],
                winner= True if row["winner"] == 'yes' else False,
            )

            # Se não existir ele insere
            if movie_exists.first() is None:
                movie = Movie(
                    year=row["year"],
                    title=row["title"],
                    studios=row["studios"],
                    producers=row["producers"],
                    winner= True if row["winner"] == 'yes' else False,
                )

                # Adiciona o objeto Movie à sessão do banco de dados            #     
                db.add(movie)

        # Adiciona os objetos Movie à sessão do banco de dados        
        if movie:
            log.info(f'Commitando o banco de dados...')
            db.commit()
        
    except Exception as e:
        log.error(f'Erro ao importar dados para o banco de dados. Erro: {str(e)}')
        # Cancelando os lançamentos no BD
        db.rollback()
        raise ValueError(f"Erro ao importar dados para o banco de dados. Erro: {str(e)}")

    
