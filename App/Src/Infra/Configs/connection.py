from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from .config import ConfigDatabase


class DBConnectionHandler:
    __CONNECTION_STRING = ConfigDatabase.config()

    def __init__(self):
        self.__connection_string = self.__CONNECTION_STRING
        self.__engine = self.__create_engine()
        self.session = None
        self.create_base_engine()
        self.create_table()

    def create_base_engine(self):
        engine = create_engine(self.__connection_string, echo=True)

        try:
            engine.connect()
        except Exception as e:
            if '1049' in str(e):
                engine = create_engine(self.__connection_string.rsplit('/', 1)[0], echo=True)
                conn = engine.connect()
                conn.execute(f"CREATE DATABASE IF NOT EXISTS {self.__connection_string.rsplit('/', 1)[1]};")
                conn.close()
            else:
                raise e

    def __create_engine(self):
        engine = create_engine(self.__connection_string)

        return engine

    def get_engine(self):
        return self.__engine

    def create_table(self):
        engine = self.__create_engine()
        conn = engine.connect()
        Base.metadata.create_all(engine, checkfirst=True)
        print('tabelas criadas')
        conn.close()

    def __enter__(self):
        session_maker = sessionmaker(bind=self.__engine)
        self.session = session_maker()
        print('Gerando conexão')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Fechando conexao')
        self.session.close()
