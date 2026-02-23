from dataclasses import dataclass
from environs import Env
from enum import Enum
import sys

class AppMode(str, Enum):
    """Допустимые режимы работы приложения"""
    PROD = "PROD"
    DEV = "DEV"

@dataclass
class DatabaseConfig:
    database_url: str

@dataclass
class DocsConfig:
    user: str
    password: str


@dataclass
class Config:
    database: DatabaseConfig
    secret_key: str
    debug: bool
    mode: str
    docs: DocsConfig


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        database=DatabaseConfig(database_url=env("DATABASE_URL")),
        secret_key=env("SECRET_KEY"),
        debug=env.bool("DEBUG", default=False),
        mode=AppMode(env("MODE")),
        docs=DocsConfig(user=env("DOCS_USER"), password=env("DOCS_PASSWORD")),
    )
