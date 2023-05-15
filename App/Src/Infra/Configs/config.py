from configparser import ConfigParser
import os


class ConfigDatabase:
    @classmethod
    def config(cls, section='postgresql') -> str:
        path = ['Src', 'Infra', 'Configs', 'database.ini']
        full_file_path = os.path.join(os.getcwd(), *path)

        parser = ConfigParser()
        parser.read(full_file_path)

        if parser.has_section(section):
            params = parser.items(section)

            db = {param[0]: param[1] for param in params}

            return cls.__get_string_connection(db)

        else:
            raise Exception(f'Section {section} not found in the {full_file_path}')

    @staticmethod
    def __get_string_connection(db: dict) -> str:
        pattern = 'dialect+driver://username:password@host:port/database'

        for key, value in db.items():
            pattern = pattern.replace(key, value)

        return pattern
