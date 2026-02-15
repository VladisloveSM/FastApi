from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.models import Feedback, User
from passlib.context import CryptContext
import secrets

app = FastAPI()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("secretpassword")
    },
    "user": {
        "username": "user",
        "hashed_password": pwd_context.hash("userpass123")
    }
}

feedbacks = []

def auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = fake_users_db.get(credentials.username)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    username_matches = secrets.compare_digest(
        credentials.username.encode("utf-8"),
        user["username"].encode("utf-8")
    )
    
    if not username_matches:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    password_correct = pwd_context.verify(
        credentials.password, 
        user["hashed_password"]
    )
    
    if not password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return user


@app.post("/feedback")
async def create_feedback(feedback: Feedback, is_premium: bool = False):
    feedbacks.append(feedback)
    if is_premium:
        message = f"Thank you, {feedback.name}! Your feedback has been saved. Your feedback will be reviewed with priority."
    else:
        message = f"Thank you, {feedback.name}! Your feedback has been saved."
    return { "message": message }


@app.get("/comments")
async def read_feedbacks():
    return feedbacks
