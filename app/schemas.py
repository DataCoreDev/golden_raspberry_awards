from pydantic import BaseModel
from typing import List

#Classe para a resposta do endpoint de produtores
class Producer_Interval(BaseModel):
    producer : str
    interval : int
    previousWin : int
    followingWin : int

#Classe para a resposta do endpoint de intervalos
class Interval_Response(BaseModel):
    min : List[Producer_Interval]
    max : List[Producer_Interval]