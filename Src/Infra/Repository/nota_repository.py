from sqlalchemy.testing import db_spec

from Src.Infra.Configs.connection import DBConnectionHandler
from Src.Infra.Entities.nota import Nota


class NotaRepository:
    @staticmethod
    def select():
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).all()
            return data

    @staticmethod
    def insert(nome, data, texto):
        kwargs = {'nome': nome, 'data': data, 'texto': texto}
        with DBConnectionHandler() as db:
            data_insert = Nota(**kwargs)
            db.session.add(data_insert)
            db.session.commit()

    @staticmethod
    def delete(id):
        with DBConnectionHandler as db:
            db.session.query(Nota).filter(Nota.id == id).delete()
            db.session.commit()

    @staticmethod
    def update(id, nome, texto):
        kwargs = {'nome': nome, 'texto': texto}
        with DBConnectionHandler() as db:
            db.session.query(Nota).filter(Nota.id == id).update(kwargs)
            db.session.commit()
