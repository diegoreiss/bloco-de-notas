from Src.Infra.Configs.base import Base
from sqlalchemy import \
    Column, String, Integer, \
    DateTime


class Nota(Base):
    __tablename__ = 'nota'

    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String, nullable=False)
    data = Column(DateTime, nullable=False)
    texto = Column(String, nullable=False)
    data_criacao = Column(DateTime, default="NOW()", nullable=False)

    def __repr__(self):
        return str(self.__dict__)

