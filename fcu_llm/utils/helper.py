# Code by AkinoAlice@TyrantRey

from utils.setup import SetupMYSQL, SetupMilvus
from utils.error import *

from os import getenv

import logging

class MySQLHandler(SetupMYSQL):
    def __init__(self) -> None:
        super().__init__()

    def uploaded_file(self, file_uuid: str = "", filename: str = "") -> bool:
        logging.info(filename)
        self.cursor.execute("""
            INSERT INTO file (file_id, file_name)
            VALUES (
                %s, %s
            );""", (file_uuid, filename,))
        self.close_connection()

        return True

    def close_connection(self, commit_sql: bool=True) -> bool:
        try:
            if commit_sql:
                logging.debug(f"committed sql: {self.cursor}")
                self.connection.commit()
        except Exception as error:
            logging.error(error)
            self.connection.rollback()
            return False
        finally:
            logging.debug("Mysql connection closed")
            self.connection.close()
            return True

class MilvusHandler(SetupMilvus):
    def __init__(self) -> None:
        super().__init__()

class RAGHandler(object):
    def __init__(self) -> None:
        ...

    def ask_question(self, question: str = "") -> str:
        ...
        return

class EncoderHandler(object):
    def __init__(self) -> None:
        ...

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("./.env")
