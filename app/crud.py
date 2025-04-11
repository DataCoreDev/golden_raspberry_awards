from collections import defaultdict
from app.models import Movie

####################
# Comentários do código sendo mostrados no log
####################

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
            producers = winner.producers.split(",")
            for producer in producers:
                producers_years[producer.strip()].append(winner.year)

        # Dicionário que irá armazenar os intervalos
        intervals = []

        log.info(f'Iterando sobre os items da lista anterior...')
        for producer, years in producers_years.items():
            sorted_years = sorted(years)

            log.info(f'Montando o dicionário e fazendo os cálulos de intervalos...')
            for year_count in range(len(sorted_years) - 1):
                intervals.append({
                    "producer" : producer,
                    "interval" : years[year_count + 1] - years[year_count],
                    "previousWin" : years[year_count],
                    "followinWin" : years[year_count + 1],
                })

        if intervals == []:
            log.info(f'Não existem intervalos.')
            return {"max": [], "min": []}
        
        # Inicializa as variáveis com o primeiro intervalo da lista
        min_interval = intervals[0]["interval"]
        max_interval = intervals[0]["interval"]

        for interval in intervals:
            if interval["interval"] < min_interval:
                min_interval = interval["interval"]
            if interval["interval"] > max_interval:
                max_interval = interval["interval"]

        log.info(f'Relatório de intervalos pronto...')
        
        return {
            "max": [interval for interval in intervals if interval["interval"] == max_interval],
            "min": [interval for interval in intervals if interval["interval"] == min_interval],
        }        
        

    except Exception as e:
        log.error(f'Erro ao gerar relatório de intervalos. Erro: {str(e)}')
        raise ValueError(f'Erro ao gerar relatório de intervalos. Erro: {str(e)}')