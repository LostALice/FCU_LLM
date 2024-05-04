# Code by AkinoAlice@TyrantRey

from langchain_community.document_loaders import PyPDFLoader

from utils.setup import SetupMYSQL, SetupMilvus
from utils.error import *

from text2vec import SentenceModel
from llama_cpp import Llama
from pprint import pformat
from numpy import ndarray

import logging
import opencc
import os


class MySQLHandler(SetupMYSQL):
    def __init__(self) -> None:
        super().__init__()

    def insert_file(self, file_uuid: str, filename: str, tags: str, collection: str) -> bool:
        logging.debug(
            pformat(f"insert_file {file_uuid} {filename} {tags} {collection}"))

        self.cursor.execute("""
            INSERT INTO file (file_id, file_name, tags, collection)
            VALUES (
                %s, %s, %s, %s
            );""", (file_uuid, filename, tags, collection))

        return self.commit()

    def insert_chatting(
        self,
        chat_id: str,
        qa_id: str,
        question: str,
        answer: str,
        token_size: int,
        sent_by: str,
        file_ids: list[str] | None = None,
    ) -> bool:

        logging.debug(pformat({
            "chat_id": chat_id,
            "qa_id": qa_id,
            "question": question,
            "answer": answer,
            "token_size": token_size,
            "sent_by": sent_by,
            "file_ids": file_ids,
        }))

        self.cursor.execute("""
            INSERT INTO `FCU_LLM`.`qa` (chat_id, qa_id, question, answer, token_size, sent_by)
            VALUES (
                %s, %s, %s, %s, %s, %s
            );
        """, (chat_id, qa_id, question, answer, token_size, sent_by))

        success = self.commit()

        if not success:
            return success

        if not file_ids is None:
            for file_id in set(file_ids):
                self.cursor.execute("""
                    INSERT INTO `FCU_LLM`.`attachment` (chat_id, qa_id, file_id)
                    VALUES (
                        %s, %s, %s
                    );
                """, (chat_id, qa_id, file_id))
            success = self.commit()
            assert success

        return success

    def commit(self, commit_sql: bool = True) -> bool:
        try:
            if commit_sql:
                logging.debug(pformat(
                    f"committed sql: {str(self.cursor.statement)}"
                ))
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
        file_uuid: str,
        collection: str = "default",
        remove_duplicates: bool = True
    ) -> dict:
        # fix duplicates
        if remove_duplicates:
            is_duplicates = self.milvus_client.query(
                collection_name=collection,
                filter=f"""(source == "{pdf_filename}
                            ") and (content == "{content}")"""
            )

            if is_duplicates:
                info = self.milvus_client.delete(
                    collection_name="default",
                    ids=[i["id"] for i in is_duplicates]
                )
                logging.debug(pformat(f"Deleted: {info}"))

        success = self.milvus_client.insert(
            collection_name=collection,
            data={
                "source": str(pdf_filename),
                "vector": vector,
                "content": content,
                "file_uuid": file_uuid
            }
        )

        return success

    def search_similarity(
        self,
        question_vector: ndarray,
        collection_name: str = "default",
        limit: int = 10
    ) -> dict[list[str], list[str], list[int]]:

        docs_results = self.milvus_client.search(collection_name=collection_name, data=[
                                                 question_vector], limit=limit)[0]
        logging.info(f"docs_results: {docs_results}")

        regulations = {
            "source": [],
            "content": [],
            "file_uuid": [],
        }

        for _ in docs_results:
            file_ = self.milvus_client.get(
                collection_name="default",
                ids=_["id"],
            )[0]

            regulations["source"].append(file_["source"])
            regulations["content"].append(file_["content"])
            regulations["file_uuid"].append(file_["file_uuid"])

        logging.debug(pformat(regulations))

        return regulations


class FileHandler(object):
    def __init__(self) -> None:
        ...

    def pdf_splitter(self, document_path: str) -> list[str]:
        if not document_path.endswith(".pdf"):
            raise FormatError("Supported formats: .pdf")

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
        self.model = Llama(
            model_path=f"""./model/{os.getenv("LLM_MODEL")}""",
            verbose=False,
            n_gpu_layers=-1,
            n_ctx=0,
        )

        self.system_prompt = "你是一個逢甲大學的學生助理，你只需要回答關於學分，課程，老師等有關資料，不需要回答學分，課程，老師以外的問題。你現在有以下資料 {regulations} 根據上文回答問題"

        self.converter = opencc.OpenCC("s2tw.json")

    def token_counter(self, prompt: str) -> int:
        return len(self.model.tokenize(prompt.encode("utf-8")))

    def response(self, question: str, regulations: list, max_tokens: int = 8192):
        content = self.system_prompt.format(regulations=" ".join(regulations))

        token_count = self.token_counter(content)

        message = [
            {
                "role": "system",
                "content": content,
            },
            {
                "role": "user",
                "content": question
            },
        ]

        output = self.model.create_chat_completion(
            message,
            stop=["<|eot_id|>", "<|end_of_text|>"],
            max_tokens=max_tokens,
        )["choices"][0]["message"]["content"]

        return self.converter.convert(output), token_count


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("./.env")

    VectorHandler().encoder("學分的抵免原則")
    MilvusHandler().search_similarity()
