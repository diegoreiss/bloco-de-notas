from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:
    def __init__(self):
        self.__connection_string = 'postgresql+psycopg2://postgres:1710@localhost/blocodenotas'
        self.__engine = self.create_database_engine()
        self.session = None
        self.__create_database()

    def create_database(self):
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

    def __enter__(self):
        session_maker = sessionmaker(bind=self.__engine)
        print('Gerando conexão')
        self.session = session_maker()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Fechando conexao')
        self.session.close()
