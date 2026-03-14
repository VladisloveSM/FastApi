import secrets
from fastapi import HTTPException
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

def get_user(username: str, password: str):
    for user in USERS_DATA:
        if secrets.compare_digest(user.get("username").encode("utf-8"), username.encode("utf-8")):
            if pwd_context.verify(password, user.get("password")):
                return True
            else:
                raise HTTPException(status_code=401, detail=f"Authorization failed")
    raise HTTPException(status_code=404, detail="User not found")
