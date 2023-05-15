from sqlalchemy import \
    Column, String, Integer, \
    Date
from sqlalchemy.sql import func
from ..Configs.base import Base


class Nota(Base):
    __tablename__ = 'nota'

    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String, nullable=False)
    texto = Column(String, nullable=False)
    data_criacao = Column(Date, server_default=func.now())

    def __repr__(self):
        return str(self.__dict__)
