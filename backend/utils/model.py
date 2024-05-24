# Code by AkinoAlice@TyrantRey


from pydantic import BaseModel


class QuestioningModel(BaseModel):
    chat_id: str
    question: str
    user_id: str
    collection: str = "default"