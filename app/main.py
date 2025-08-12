import logging

from fastapi import FastAPI

from app import config
from app.config import load_config
from app.logger import logger


app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = load_config()
if config.debug:
    app.debug = True
else:
    app.debug = False


@app.get("/")
def read_root():
    logger.info("Handling request to root endpoint")
    return {"message": "Hello, World!"}


@app.get("/db")
def get_db_info():
    logger.info(f"Connecting to database with URL: {config.db.database_url}")
