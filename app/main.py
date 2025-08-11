# обновляем код main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    message: str

@app.post("/")
def root(user: User):
    print(f"Received user: {user.username} with message: {user.message}")
    return user