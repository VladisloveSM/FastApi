from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

refresh_tokens = {}

USERS_DATA = [
    {
        "username": "admin",
        "password": pwd_context.hash("admin")
    },
    {
        "username": "user",
        "password": pwd_context.hash("user")
    },
    {
        "username": "pass",
        "password": pwd_context.hash("pass")
    },
]
