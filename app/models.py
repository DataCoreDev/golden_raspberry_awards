from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

#Tabela criada com base no arquivo movies.csv
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    title = Column(String)
    studios = Column(String)
    producers = Column(String)
    winner = Column(Boolean, default=False)
