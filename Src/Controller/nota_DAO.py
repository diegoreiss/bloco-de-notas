import sqlite3
import os


class NotaDAO:
    def __init__(self, db_name='database.db'):
        self.connection = None
        self.db_name = db_name

    def create_tables(self):
        try:
            os.chdir('../bd/')

            with open('Script.sql', 'r') as sql_file:
                script = sql_file.read()

            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(script)
            print('tabela criada')
        except sqlite3.Error as e:
            print(e)
        except BaseException as e:
            print(e)
        finally:
            self.close_connection()

    def connect(self):
        try:
            os.chdir('../bd/')
            self.connection = sqlite3.connect(self.db_name)
        except sqlite3.Error as e:
            print(e)

    def close_connection(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(e)

    def registrar_nota(self, nota):
        campos_nota = tuple(vars(nota).keys())[1:]
        valores_nota = [nota.nome, nota.texto, nota.categoria_id]

        try:
            self.connect()
            cursor = self.connection.cursor()

            script = f"""
                INSERT INTO 
                    nota {campos_nota}
                VALUES (?, date('now'), ?, ?);
            """

            cursor.execute(script, valores_nota)
            self.connection.commit()

            return 'inserted'
        except sqlite3.Error as e:
            return e
        except BaseException as e:
            return e
        finally:
            self.close_connection()

    def atualizar_nota(self, nota):
        valores_nota = (nota.nome, nota.texto, nota.id)

        try:
            self.connect()
            cursor = self.connection.cursor()
            script = f"""
                UPDATE 
                    nota
                SET
                    nome = ?,
                    texto = ?
                WHERE
                    id = ?
            """

            cursor.execute(script, valores_nota)
            self.connection.commit()

            return 'updated'
        except sqlite3.Error as e:
            return e
        except BaseException as e:
            print(e)
        finally:
            self.close_connection()

    def remover_nota(self, nota):
        try:
            self.connect()
            cursor = self.connection.cursor()
            script = f"""
                DELETE FROM nota
                WHERE id = ?;
            """

            cursor.execute(script, (nota.id,))
            self.connection.commit()

            return 'deleted'
        except sqlite3.Error as e:
            return e
        except BaseException as e:
            return e
        finally:
            self.close_connection()

    def consultar_todas_notas(self):
        self.connect()

        script = f"""
            SELECT 
                n.id, 
                n.nome,
                strftime('%d/%m/%Y', n.data),
                n.texto,
                strftime('%d/%m/%Y %H:%M:%S', n.last_update),
                c.nome
            FROM
                nota n
            INNER JOIN categoria c
            ON 
                n.categoria_id = c.id;
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(script)
            notas = cursor.fetchall()

            return notas
        except sqlite3.Error as e:
            print(e)
        except BaseException as e:
            print(e)
        finally:
            self.close_connection()

    def consultar_nome_categoria(self):
        try:
            self.connect()
            cursor = self.connection.cursor()

            script = f"""
            
                SELECT nome FROM categoria;
            """

            cursor.execute(script)

            return cursor.fetchall()
        except sqlite3.Error as e:
            return e
        except BaseException as e:
            return e
        finally:
            self.close_connection()

    def consultar_todas_categorias(self):
        try:
            self.connect()
            cursor = self.connection.cursor()

            script = f"""
                SELECT 
                    *
                FROM
                    categoria;
            """

            cursor.execute(script)
            return cursor.fetchall()
        except sqlite3.Error as e:
            return e
        except BaseException as e:
            return e
        finally:
            self.close_connection()
