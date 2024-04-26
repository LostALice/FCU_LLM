# Code by AkinoAlice@TyrantRey

from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate

from utils.setup import SetupMYSQL, SetupMilvus
from utils.error import *

from text2vec import SentenceModel
from numpy import ndarray
from typing import Union
from os import getenv

import logging


class MySQLHandler(SetupMYSQL):
    def __init__(self) -> None:
        super().__init__()

    def uploaded_file(self, file_uuid: str = "", filename: str = "") -> bool:
        logging.info("uploaded_file", filename)
        self.cursor.execute("""
            INSERT INTO file (file_id, file_name)
            VALUES (
                %s, %s
            );""", (file_uuid, filename,))
        self.close_connection()

        return True

    def insert_file(self, file_uuid: str, filename: str, tags: list[str]) -> bool:
        logging.info("insert_file", file_uuid, filename, tags)
        self.cursor.execute("""
            INSERT INTO file (file_id, file_name)
            VALUES (
                %s, %s
            );""", (file_uuid, filename,))

        self.close_connection()

    def close_connection(self, commit_sql: bool = True) -> bool:
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

    def insert_sentence(
        self,
        pdf_file_name: str,
        vector: ndarray,
        content: str,
        collection: str = "default"
    ) -> dict:
        success = self.client.insert(
            collection_name=collection,
            data={
                "source": str(pdf_file_name),
                "vector": vector,
                "content": content,
            }
        )

        return success["ids"][0]

    def search(self, data: ndarray, collection: str, num_of_return: int = 5) -> Union[str, None]:
        ...

    def get_data(self, collection: str, ids: int) -> list[int, str, str]:
        ...


class RAGHandler(MilvusHandler):
    def __init__(self) -> None:
        super().__init__()

    def ask_question(self, question: str) -> str:
        return


class TextHandler(object):
    def __init__(self) -> None:
        ...

    def pdf_splitter(self, document_path: str) -> list[str]:
        if not document_path.endswith(".pdf"):
            raise FileFormatError("Supported formats: .pdf")

        pdf = PyPDFLoader(document_path)
        all_splits = pdf.load_and_split()
        splitted_content = "".join([text.page_content.replace("\n", "").replace(" ", "")
                                    for text in all_splits]).split("。")

        # last element is ""
        return splitted_content[:-1]

    def question_splitter(self, question: str) -> str:
        ...


class VectorHandler(object):
    def __init__(self) -> None:
        self.HF_embedding_model = getenv("HF_EMBEDDING_MODEL")
        self.embedding = SentenceModel(self.HF_embedding_model)

    def encoder(self, text: str) -> ndarray:
        return self.embedding.encode(text)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("./.env")
