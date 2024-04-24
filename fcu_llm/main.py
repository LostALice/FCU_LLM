# Code by AkinoAlice@TyrantRey

from fastapi import UploadFile, Form
from fastapi import HTTPException
from fastapi import FastAPI

from utils.helper import (
    EncoderHandler,
    MySQLHandler,
    MilvusHandler,
    RAGHandler,
    TextHandler,
    VectorHandler
)
from utils.error import *

import logging
import uuid

logging.level = logging.DEBUG

app = FastAPI(debug=True)


@app.get("/", status_code=200)
async def test():
    return HTTPException(status_code=200, detail="ok")


@app.post("/login/", status_code=200)
async def login():
    return HTTPException(status_code=200, detail="ok")


@app.post("/upload/", status_code=200)
async def file_upload(pdf_file: UploadFile, tags: list[str] = Form()):
    if not pdf_file.filename.endswith(".pdf"):
        logging.info(f"Invalid file type: {pdf_file.filename}")
        return HTTPException(status_code=200, detail="Invalid file type")

    file_uuid = str(uuid.uuid4())
    success = MySQLHandler().uploaded_file(file_uuid=file_uuid, filename=pdf_file.filename)

    # save uploaded pdf file
    pdf_contents = pdf_file.file.read()
    with open(f"./files/{file_uuid}.pdf", "wb") as f:
        f.write(pdf_contents)

    logging.info(f"file uploaded: {success}")

    # load sentences from pdf
    docs_loader = TextHandler()
    splitted_content = docs_loader.pdf_splitter(f"./files/{file_uuid}.pdf")

    # insert to milvus
    milvus_client = MilvusHandler()
    mysql_client = MySQLHandler()
    text2vector = VectorHandler()

    # to be
    # for sentence in splitted_content:
    #     vector = text2vector.encoder(sentence)
    #     sentence_id = milvus_client.insert_sentence(
    #         vector=vector, pdf_file_name=pdf_file.filename, content=sentence)
    #     mysql_client.insert_file()

    if success:
        return {
            "success": success,
            "file_id": file_uuid,
        }
    return HTTPException(status_code=200, detail="Internal server error")

@app.post("/question/", status_code=200)
async def question(question: str = ""):
    return f"your question: {question}"

if __name__ == "__main__":
    # development only
    # uvicorn main:app --reload --host 0.0.0.0 --port 8080
    app.run(debug=True)
