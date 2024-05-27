# Code by AkinoAlice@TyrantRey

from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, Form
from fastapi import HTTPException
from fastapi import FastAPI

from utils.helper import (
    VectorHandler,
    MilvusHandler,
    MySQLHandler,
    FileHandler,
    RAGHandler,
)
from utils.model import (
    QuestioningModel
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
logging.debug(f"""Debug {os.getenv("DEBUG")}""")

# disable logging
logging.getLogger("multipart").propagate = False

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UtilsLoader(object):
    def __init__(self) -> None:
        self.milvus_client = MilvusHandler()
        self.mysql_client = MySQLHandler()
<<<<<<< HEAD

=======
>>>>>>> backend
        self.encoder_client = VectorHandler()
        self.docs_client = FileHandler()
        self.RAG = RAGHandler()


LOADER = UtilsLoader()

logging.debug("====================")
logging.debug("| loading finished |")
logging.debug("====================")

@app.get("/", status_code=200)
async def test():
    return HTTPException(status_code=200, detail="test ok")


@app.post("/login/", status_code=200)
async def login():
    return HTTPException(status_code=200, detail="login")

@app.get("/uuid/")
async def get_uuid() -> str:
    uuid_ = str(uuid.uuid4())
    print(uuid_)
    return uuid_

@app.post("/upload/", status_code=200)
async def file_upload(docs_file: UploadFile, tags: list[str] = Form(), collection: str = "default"):
    """upload a docs file

    Args:
        docs_file (UploadFile): docs file
        tags (list[str], optional): file tags. Defaults to Form().
        collection (str, optional): insert into collection. Defaults to "default".

    Returns:
        file_id: file uuid
    """
    file_tags = str(json.dumps({"tags": tags}))
    filename = str(docs_file.filename)
    file_uuid = str(uuid.uuid4())

    logging.debug(
        pformat(f"""docs_file: {filename} file_uuid: {file_uuid} tags: {file_tags}"""))

    # exclude non pdf files
    if not filename.endswith(".pdf"):
        logging.debug(pformat(f"Invalid file type: {filename}"))
        return HTTPException(status_code=200, detail="Invalid file type")

    # save uploaded pdf file
    pdf_contents = docs_file.file.read()
    with open(f"./files/{file_uuid}.pdf", "wb") as f:
        f.write(pdf_contents)

    # load sentences from pdf
    splitted_content = LOADER.docs_client.pdf_splitter(
        f"./files/{file_uuid}.pdf")
    logging.debug(pformat(splitted_content))

    # insert to milvus
    for sentence in splitted_content:
        vector = LOADER.encoder_client.encoder(sentence)
        insert_info = LOADER.milvus_client.insert_sentence(
            docs_filename=filename,
            vector=vector,
            content=sentence,
            file_uuid=file_uuid,
            collection=collection
        )

        logging.debug(pformat(insert_info))

    success = LOADER.mysql_client.insert_file(
        file_uuid=file_uuid, filename=filename, tags=file_tags, collection=collection)

    if success:
        return {
            "success": success,
            "file_id": file_uuid,
        }

    return HTTPException(status_code=200, detail="Internal server error")


@app.post("/chat/{chat_id}", status_code=200)
async def questioning(question_model:QuestioningModel):
    """Ask the question and return the answer from RAG

    Args:
        chat_id (str): chatroom uuid
        question (str): question content
        user_id (str): user id
        collection (str, optional): collection of docs database. Defaults to "default".

    Returns:
        answer: response of the question
        server_status_code: 200 | 500
    """
    chat_id = question_model.chat_id
    question = question_model.question
    user_id = question_model.user_id
    collection = question_model.collection
    question_uuid = str(uuid.uuid4())

    logging.debug(pformat({
        "chat_id": chat_id,
        "question": question,
        "user_id": user_id,
        "collection": collection,
        "question_uuid": question_uuid
    }))

    # search question
    question_vector = LOADER.encoder_client.encoder(question)
    regulations = LOADER.milvus_client.search_similarity(
        question_vector, collection_name=collection)
    answer, token_size = LOADER.RAG.response(
        regulations=regulations["content"], question=question)

    # insert into mysql
    LOADER.mysql_client.insert_chatting(
        chat_id=chat_id,
        qa_id=question_uuid,
        answer=answer,
        question=question,
        token_size=token_size,
        sent_by=user_id,
        file_ids=regulations["file_uuid"]
    )

    if answer:
        return {
            "question_uuid": question_uuid,
            "answer": answer,
            "file_ids": set(regulations["source"]),
        }

    return HTTPException(status_code=200, detail="Internal server error")

if __name__ == "__main__":
    # development only
    # uvicorn main:app --reload --host 0.0.0.0 --port 8080
    app.run(debug=os.getenv("DEBUG"))
