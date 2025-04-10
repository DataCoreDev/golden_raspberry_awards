import pandas as pd
from datetime import datetime
from app.models import Movie

# Função para importar o arquivo CSV e salvar no banco de dados
def import_movie_list(path, db):
    # Primeiro verificar se o aquivo antes de importar, se não existir retorna um erro
    try:
        csv_file = pd.read_csv(path)
    except Exception as e:
        raise FileNotFoundError(f"Erro ao carregar arquivo. Erro: {e.message}")
    
    # Verifica se o arquivo está vazio
    if csv_file.empty:
        raise ValueError("Arquivo CSV vazio.")
    
    # Verifica se as colunas necessárias estão presentes
    required_columns = ["year", "title", "studios", "producers", "winner"] 
    for col in required_columns:
        if col not in csv_file.columns:
            raise ValueError(f"Coluna {col} não encontrada no arquivo CSV.")
        
    try:
        # Converte o DataFrame para uma lista de dicionários    
        data = csv_file.to_dict(orient="records") 
        movie = None       

        # Iterando sobre os dados e criando os Movies
        for row in data:
            # Buscando no BD se o filme já existe
            movie_exists = db.query(Movie).filter_by(
                year=row["year"],
                title=row["title"],
                studios=row["studios"],
                producers=row["producers"],
                winner=row["winner"]
            )

            # Se não existir ele insere
            if movie_exists.first() is None:
                movie = Movie(
                    year=row["year"],
                    title=row["title"],
                    studios=row["studios"],
                    producers=row["producers"],
                    winner=row["winner"]
                )

                # Adiciona o objeto Movie à sessão do banco de dados            #     
                db.add(movie)

        # Adiciona os objetos Movie à sessão do banco de dados        
        if movie:
            db.commit()
        
    except Exception as e:
        #Cancelando os lançamentos no BD
        db.rollback()
        raise ValueError(f"Erro ao importar dados para o banco de dados. Erro: {e.message}")

    
