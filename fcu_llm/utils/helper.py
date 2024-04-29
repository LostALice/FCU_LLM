# Code by AkinoAlice@TyrantRey

from langchain_community.document_loaders import PyPDFLoader
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate

from utils.setup import SetupMYSQL, SetupMilvus
from utils.error import *

from text2vec import SentenceModel
# from llama_cpp import Llama
from pprint import pformat
from numpy import ndarray
from typing import Union

import logging
import opencc
import os

class MySQLHandler(SetupMYSQL):
    def __init__(self) -> None:
        super().__init__()

    def insert_file(self, file_uuid: str, filename: str, tags: str) -> bool:
        logging.debug(pformat("insert_file {file_uuid} {filename} {tags}"))
        self.cursor.execute("""
            INSERT INTO file (file_id, file_name, tags)
            VALUES (
                %s, %s, %s
            );""", (file_uuid, filename, tags))

        return self.commit()

    def insert_chatroom(self, message: str, chatroom_id: str) -> bool: ...

    def commit(self, commit_sql: bool = True) -> bool:
        try:
            if commit_sql:
                logging.debug(pformat(f"committed sql: {str(self.cursor.statement)}"))
                self.connection.commit()
        except Exception as error:
            logging.error(error)
            self.connection.rollback()
            return False
        finally:
            logging.debug(pformat("Mysql committed"))
            return True




class MilvusHandler(SetupMilvus):
    def __init__(self) -> None:
        super().__init__()

    def insert_sentence(
        self,
        pdf_filename: str,
        vector: ndarray,
        content: str,
        collection: str = "default",
        remove_duplicates: bool = True
    ) -> dict:
        # fix duplicates
        if remove_duplicates:
            is_duplicates = self.milvus_client.query(
                collection_name=collection,
                filter=f"""(source == "{pdf_filename}") and (content == "{content}")"""
            )

            if is_duplicates:
                info = self.milvus_client.delete(
                    collection_name="default",
                    ids=[i["id"] for i in is_duplicates]
                )
                logging.debug(pformat(f"Deleted: {info} {is_duplicates}"))

        success = self.milvus_client.insert(
            collection_name=collection,
            data={
                "source": str(pdf_filename),
                "vector": vector,
                "content": content,
            }
        )

        return success

    def search_similarity(self, question_vector: ndarray, collection_name: str ="default", limit: int = 10) -> dict[list, list]:
        docs_results = self.milvus_client.search(collection_name=collection_name, data=[question_vector], limit=limit)[0]
        logging.info(f"docs_results: {docs_results}")

        regulations = {
            "source": [],
            "content": [],
        }

        for _ in docs_results:
            file_ = self.milvus_client.get(
                collection_name="default",
                ids=_["id"],
            )[0]

            regulations["source"].append(file_["source"])
            regulations["content"].append(file_["content"])

        logging.debug(pformat(regulations))

        return regulations


class DocsHandler(object):
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


class VectorHandler(object):
    def __init__(self) -> None:
        self.HF_embedding_model = os.getenv("HF_EMBEDDING_MODEL")
        self.embedding = SentenceModel(self.HF_embedding_model)

    def encoder(self, text: str) -> ndarray:
        return self.embedding.encode(text)


class RAGHandler(object):
    def __init__(self) -> None:
        self.template = "你是一個逢甲大學的學生助理，你只需要回答關於學分，課程，老師等有關資料，不需要回答學分，課程，老師以外的問題。你現在有以下資料 {context} 根據上文回答問題: {question} 你的回答"
        self.prompt_template = PromptTemplate.from_template(self.template)

        self.llm_model = f"""./model/{os.getenv("LLM_MODEL")}"""
        if not os.path.isfile(self.llm_model):
            logging.error(pformat("FileNotFoundError"))
            raise FileNotFoundError

        self.llm = LlamaCpp(
            model_path=f"""./model/{os.getenv("LLM_MODEL")}""",
            n_gpu_layers=-1,
            n_ctx=0,
            verbose=True
        )
        self.converter = opencc.OpenCC("s2tw.json")

    def answering(self, regulations: list, question: str) -> str:
        rag_chain = (
            {
                "context": lambda x: regulations,
                "question": RunnablePassthrough()
            }
            | self.prompt_template
            | self.llm
        )
        logging.info(pformat(rag_chain))
        llm_response = rag_chain.invoke(question)

        return self.converter.convert(llm_response)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("./.env")

    VectorHandler().encoder("人工智慧專業技術與應用學士學位學程科目的抵免原則")
    MilvusHandler().search_similarity()