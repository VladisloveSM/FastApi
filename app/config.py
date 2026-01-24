from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database_url: str


@dataclass
class Config:
    database: DatabaseConfig
    seceret_key: str
    debug: bool


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        database=DatabaseConfig(database_url=env("DATABASE_URL")),
        seceret_key=env("SECRET_KEY"),
        debug=env.bool("DEBUG", default=False),
    )
