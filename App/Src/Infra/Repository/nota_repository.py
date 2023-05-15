from ..Configs.connection import DBConnectionHandler
from ..Entities.nota import Nota


class NotaRepository:
    @staticmethod
    def select():
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).all()

            return data

    @staticmethod
    def insert(**kwargs):
        with DBConnectionHandler() as db:
            try:
                data_insert = Nota(**kwargs)
                db.session.add(data_insert)
                db.session.commit()
            except BaseException as e:
                raise e

    @staticmethod
    def delete(id):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Nota).filter(Nota.id == id).delete()
                db.session.commit()
            except BaseException as e:
                raise e

    @staticmethod
    def update(id, **kwargs):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Nota).filter(Nota.id == id).update(kwargs)
                db.session.commit()
            except BaseException as e:
                raise e
