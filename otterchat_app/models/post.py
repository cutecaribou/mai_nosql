# from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

class PostModel(BaseModel):
    author : str
    text   : str
    sent_at: datetime
