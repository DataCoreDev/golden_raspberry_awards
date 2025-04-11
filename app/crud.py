import pandas as pd
from collections import defaultdict
from app.models import Movie

####################
# Comentários do código sendo mostrados no log
####################

# Função para importar o arquivo CSV e salvar no banco de dados
def import_movie_list(path, db, log=None):
    # Primeiro verificar se o aquivo antes de importar, se não existir retorna um erro
    try:
        if log:
            log.info(f'Verificando se o arquivo existe...')

        csv_file = pd.read_csv(path, delimiter=';', quoting=3)
    except Exception as e:
        raise FileNotFoundError(f"Erro ao carregar arquivo. Erro: {e}")
    
    # Verifica se o arquivo está vazio
    if log:
        log.info(f'Verificando se o arquivo está vazio...')

    if csv_file.empty:
        raise ValueError("Arquivo CSV vazio.")
    
    # Verifica se as colunas necessárias estão presentes
    if log:
        log.info(f'Validando as colunas...')

    required_columns = ["year", "title", "studios", "producers", "winner"] 
    for col in required_columns:
        if col not in csv_file.columns:
            log.error(f'Coluna {col} não encontrada no arquivo CSV.')
            raise ValueError(f"Coluna {col} não encontrada no arquivo CSV.")
        
    try:
        # Converte o DataFrame para uma lista de dicionários
        if log:    
            log.info(f'Convertendo o dataframe...')

        data = csv_file.to_dict(orient="records") 
        movie = None       

        # Iterando sobre os dados e criando os Movies
        if log:
            log.info(f'iterando linhas...')

        for intcount, row in enumerate(data):
            # Buscando no BD se o filme já existe
            movie_exists = db.query(Movie).filter_by(
                year=row["year"],
                title=row["title"],
                studios=row["studios"],
                producers=row["producers"],
                winner= True if row["winner"] == 'yes' else False,
            ).first()

            #log.info(f'linha {intcount}...')

            # Se não existir ele insere
            if movie_exists is None:
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
            if log:
                log.info(f'Commitando o banco de dados...')

            db.commit()
        
    except Exception as e:
        if log:
            log.error(f'Erro ao importar dados para o banco de dados. Erro: {str(e)}')
            
        # Cancelando os lançamentos no BD
        db.rollback()
        raise ValueError(f"Erro ao importar dados para o banco de dados. Erro: {str(e)}")

def report_intervals(db, log):
    try:
        
        log.info(f'Verificando se existem dados no BD...')
        if db.query(Movie).count() == 0:
            log.info(f'Não existem dados no banco de dados.')
            raise ValueError("Não existem dados no banco de dados.")
        
        log.info(f'Buscando todos os filmes vencedores...')
        winners = db.query(Movie).filter_by(winner = True).all()
        producers_years = defaultdict(list)

        log.info(f'Iterando sobre os filme vencedores e acumulando na lista de producers_years...')
        for winner in winners:
            # Gerando um dicionário temporário para armazenar os produtores e possíveis , e and
            producers_temp = []
            
            # Verifica se tem , no campo para saber se tem mais de 1 produtor
            if "," in winner.producers:
                producers_temp = winner.producers.split(",")
            else:
                producers_temp = [winner.producers]

            # Verifica se tem and no campo para saber se tem mais de 1 produtor
            for producer in producers_temp:            
                if " and " in producer:
                    producers_temp += producer.split(" and ")

            producers = []

            # Acumulando no dicionário de producers
            for temp in producers_temp:
                if (temp.strip() not in producers) and (not "," in temp.strip()) and (not "and" in temp.strip()):
                    producers.append(temp.strip())

            for producer in producers:
                if producer.strip():
                    producers_years[producer.strip()].append(winner.year)

        # Dicionário que irá armazenar os intervalos
        intervals = []

        log.info(f'Iterando sobre os items da lista anterior...')
        for producer, years in producers_years.items():
            sorted_years = sorted(years)

            #log.info(f'Montando o dicionário e fazendo os cálulos de intervalos...')
            for year_count in range(len(sorted_years) - 1):
                intervals.append({
                    "producer" : producer,
                    "interval" : years[year_count + 1] - years[year_count],
                    "previousWin" : years[year_count],
                    "followingWin" : years[year_count + 1],
                })

        if intervals == []:
            log.info(f'Não existem intervalos.')
            return {"max": [], "min": []}
        
        # Inicializa as variáveis com o primeiro intervalo da lista
        log.info(f'Iniciando variáveis para pegar intervalo maior e menor...')
        min_interval = 99999
        max_interval = 0

        log.info(f'Iterando os intervalos para setar as variáveis de menor e maior intervalo...')
        for interval in intervals:
            if interval["interval"] < min_interval:
                min_interval = interval["interval"]
            if interval["interval"] > max_interval:
                max_interval = interval["interval"]

        log.info(f'Montando o relatório final...')
        
        return {
            "min": [interval for interval in intervals if interval["interval"] == min_interval],
            "max": [interval for interval in intervals if interval["interval"] == max_interval],            
        }        
        

    except Exception as e:
        log.error(f'Erro ao gerar relatório de intervalos. Erro: {str(e)}')
        raise ValueError(f'Erro ao gerar relatório de intervalos. Erro: {str(e)}')