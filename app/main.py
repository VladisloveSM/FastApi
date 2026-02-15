from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.models import Feedback, User, UserInDB
from passlib.context import CryptContext
import secrets

app = FastAPI()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    UserInDB(username="admin", hashed_password=pwd_context.hash("secretpassword")),
    UserInDB(username="user", hashed_password=pwd_context.hash("userpass123"))
}

feedbacks = []

def auth_user(credentials: HTTPBasicCredentials = Depends(security)):

    user = None

    for user_in_db in fake_users_db:
        if secrets.compare_digest(user_in_db.username, credentials.username):
            user = user_in_db
            break

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    password_correct = pwd_context.verify(
        credentials.password, 
        user.hashed_password
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
