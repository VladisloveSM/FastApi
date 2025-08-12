from fastapi import FastAPI

from app import config
from app.models import User
from app.config import load_config
from app.logger import logger

import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = load_config()
if config.debug:
    app.debug = True
else:
    app.debug = False

def is_adult(user: User):
    answer = user.dict()
    answer["is_adult"] = user.age >= 18
    return answer

@app.get("/")
def read_root():
    logger.info("Handling request to root endpoint")
    return {"message": "Hello, World!"}


@app.get("/db")
def get_db_info():
    logger.info(f"Connecting to database with URL: {config.database.database_url}")


@app.post("/user")
async def read_root(user: User):
    return is_adult(user)