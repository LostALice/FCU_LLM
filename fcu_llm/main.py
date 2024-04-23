# Code by AkinoAlice@TyrantRey

from fastapi import UploadFile, HTTPException
from fastapi import FastAPI

from utils.helper import EncoderHandler, MySQLHandler, MilvusHandler, RAGHandler
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
async def file_upload(pdf_file: UploadFile):
    if not pdf_file.filename.endswith(".pdf"):
        logging.info(f"Invalid file type: {pdf_file.filename}")
        return HTTPException(status_code=200, detail="Invalid file type")

    file_uuid = str(uuid.uuid4())
    success = MySQLHandler().uploaded_file(file_uuid=file_uuid, filename=pdf_file.filename)

    pdf_contents = pdf_file.file.read()
    with open("./files/{file_uuid}.pdf", "wb") as f:
        f.write(pdf_contents)

    logging.info(f"file uploaded: {success}")

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
