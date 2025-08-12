from fastapi import FastAPI

from app.models import User
from app.logger import logger

app = FastAPI()

user = User(id=1, name="John Doe")

@app.get("/users")
def read_root():
    return user
