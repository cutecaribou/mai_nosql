# from fastapi import FastAPI
from pydantic import BaseModel

class UserModel(BaseModel):
    name    : str
    email   : str
