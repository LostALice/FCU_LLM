# Code by AkinoAlice@TyrantRey

from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, Form
from fastapi import HTTPException
from fastapi import FastAPI

from utils.helper import (
    VectorHandler,
    MilvusHandler,
    MySQLHandler,
    DocsHandler,
    RAGHandler,
)

from pprint import pformat
from utils.error import *

import logging
import uuid
import json
import sys
import os

# logging
log_format = "%(asctime)s, %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
logging.basicConfig(filename="test.log", filemode="w+", format=log_format,
                    level=logging.NOTSET, encoding="utf-8")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost", "127.0.0.1"],  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UtilsLoader(object):
    def __init__(self) -> None:
        self.encoder_client = VectorHandler()
        self.milvus_client = MilvusHandler()
        self.mysql_client = MySQLHandler()
        self.docs_client = DocsHandler()
        self.RAG = RAGHandler()


LOADER = UtilsLoader()


@app.get("/", status_code=200)
async def test():
    return HTTPException(status_code=200, detail="test ok")


@app.post("/login/", status_code=200)
async def login():
    return HTTPException(status_code=200, detail="login")


@app.post("/upload/", status_code=200)
async def file_upload(pdf_file: UploadFile, tags: list[str] = Form(), collection: str = "default"):
    if not os.path.exists("./files"):
        os.mkdir("./files")

    file_tags = str(json.dumps({"tags": tags}))
    filename = str(pdf_file.filename)
    file_uuid = str(uuid.uuid4())

    logging.debug(pformat(f"""pdf_file: {filename} file_uuid: {file_uuid} tags: {file_tags}"""))

    # exclude non pdf files
    if not filename.endswith(".pdf"):
        logging.debug(pformat(f"Invalid file type: {filename}"))
        return HTTPException(status_code=200, detail="Invalid file type")

    # save uploaded pdf file
    pdf_contents = pdf_file.file.read()
    with open(f"./files/{file_uuid}.pdf", "wb") as f:
        f.write(pdf_contents)

    # load sentences from pdf
    splitted_content = LOADER.docs_client.pdf_splitter(
        f"./files/{file_uuid}.pdf")
    logging.debug(pformat(splitted_content))

    # insert to milvus
    for sentence in splitted_content:
        vector = LOADER.encoder_client.encoder(sentence)
        insert_info = LOADER.milvus_client.insert_sentence(filename, vector, sentence, collection)

        logging.debug(pformat(insert_info))

    success = LOADER.mysql_client.insert_file(
        file_uuid=file_uuid, filename=filename, tags=file_tags)

    if success:
        return {
            "success": success,
            "file_id": file_uuid,
        }

    return HTTPException(status_code=200, detail="Internal server error")


@app.post("/chat/{chat_id}", status_code=200)
async def questioning(chat_id: str, question: str,  user_id: str, collection: str = "default"):
    logging.debug(pformat(f"chat_id={chat_id} question={question}"))

    # search question
    question_vector = LOADER.encoder_client.encoder(question)
    regulations = LOADER.milvus_client.search_similarity(question_vector, collection_name=collection)
    answer = LOADER.RAG.response(regulations=regulations["content"], question=question)

    # insert into mysql
    # to be

    logging.info(pformat(answer))

    if answer:
        return HTTPException(status_code=200, detail="".join(answer))

    return HTTPException(status_code=200, detail="Internal server error")

if __name__ == "__main__":
    # development only
    # uvicorn main:app --reload --host 0.0.0.0 --port 8080
    app.run(debug=True)
