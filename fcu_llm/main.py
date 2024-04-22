# Code by AkinoAlice@TyrantRey

from fastapi import UploadFile, HTTPException
from fastapi import FastAPI

from utils.error import *

import uuid

app = FastAPI(debug=True)

@app.get("/", status_code=200)
async def test():
    return HTTPException(status_code=200, detail="ok")

@app.post("/login/", status_code=200)
async def login():
    return HTTPException(status_code=200, detail="ok")

@app.post("/upload/", status_code=200)
async def file_upload(file_: UploadFile):
    if not file_.filename.endswith(".pdf"):
        return HTTPException(status_code=200, detail="Invalid file type")

    file_id = str(uuid.uuid4())
    print(file_.filename)

    return {
        "file_id": file_id
    }

if __name__ == "__main__":
    # development only
    # uvicorn main:app --reload --host 0.0.0.0
    app.run(debug=True)