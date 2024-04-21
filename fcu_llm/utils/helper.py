# Code by AkinoAlice@TyrantRey

from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate

from setup import SetupMYSQL
from os import getenv

import mysql.connector as connector

class MySQLHandler(object):
    def __init__(self) -> None:
        self.connection = connector.connect(
            host=getenv("MYSQL_HOST"),
            user=getenv("MYSQL_USER_NAME"),
            password=getenv("MYSQL_PASSWORD"),
            port=getenv("MYSQL_PORT"),
        )

        try:
            self.connection.database=getenv("MYSQL_DATABASE")
        except connector.Error as error:
            print(error)
            SetupMYSQL()
        finally:
            self.connection.database=getenv("MYSQL_DATABASE")
            self.cursor = self.connection.cursor(dictionary=True, prepared=True)

    def file_upload(self, filename) -> bool:
        return True

class LLMHandler(object):
    def __init__(self) -> None:
        self.model = LlamaCpp(
            model_path="./LLM/chinese-alpaca-2-7b-gguf-q4_k-im.gguf",
            n_gpu_layers=-1,
            n_ctx=1024
        )

        self.prompt_template = (
            "[INST] <<SYS>>\n"
            "你是一個逢甲大學的學生助理，你只需要回答關於學分，課程，老師等有關資料，不需要回答學分，課程，老師以外的問題。\n"
            "<</SYS>>\n{question} [/INST]"
        )

        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["question"]
        )

        self.chain = self.prompt | self.model

    def ask_question(self, question: str = "") -> str:
        context = {
            "context": "你是一個逢甲大學的學生助理，你只需要回答關於學分，課程，老師等有關資料，不需要回答學分，課程，老師以外的問題。",
            "question": question
        }
        return self.chain.invoke(context)

if __name__ == "__main__":
    from dotenv import load_dotenv
    from pprint import pprint
    # load_dotenv(".env")

    llm = LLMHandler()

    pprint(llm.ask_question("什麼是學分"))

