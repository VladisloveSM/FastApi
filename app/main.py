from fastapi import FastAPI, Cookie, HTTPException, Request, Response, Depends
from app.models import Feedback, LoginData
from typing import Optional
from datetime import datetime, timedelta
from itsdangerous import BadSignature, TimestampSigner
import uuid

app = FastAPI() 

feedbacks = []

COOKIE_LIFETIME = 300  # 5 minutes in seconds
SECRET_KEY = 'supersecretkey'
signer = TimestampSigner(SECRET_KEY)

users = [
    {"id": str(uuid.uuid4()), "username": "admin", "password": "secret"},
    {"id": str(uuid.uuid4()), "username": "user", "password": "password123"},
    {"id": str(uuid.uuid4()), "username": "user123", "password": "password123"},
]


def verify_session(session_token: Optional[str] = Cookie(None)):
    if session_token is None:
        raise HTTPException(status_code=401, detail="Cookie не найдена")
    try:
        unsigned = signer.unsign(session_token, max_age=COOKIE_LIFETIME)
    except BadSignature:
        raise HTTPException(status_code=401, detail="Недействительная сессия")

    return session_token


def refresh_token(session_token: str):
    # Needs to be implemented properly in a real-world scenario
    return { "message": "Сессия обновлена" }


@app.post("/login")
async def login(data: LoginData, response: Response, session_token: Optional[str] = Cookie(None)):
    user = next(
        (u for u in users if u["username"] == data.username and u["password"] == data.password),
        None
    )
    
    if not user:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    
    # Создаём токен
    signature = signer.sign(user["id"]).decode()
    
    # Устанавливаем cookie (перезапишет если была)
    response.set_cookie(
        key="session_token",
        value=signature,
        httponly=True,
        secure=False,
        max_age=COOKIE_LIFETIME,
        samesite="lax"
    )
    
    return {"message": "Успешный вход"}


@app.get("/profile")
async def get_user(session_token: str = Depends(verify_session)):
    return {"message": f"Пользователь ваша сессия: {session_token}"}


@app.post("/feedback")
async def create_feedback(feedback: Feedback, is_premium: bool = False):
    feedbacks.append(feedback)
    if is_premium:
        message = f"Спасибо, {feedback.name}! Ваш отзыв сохранён. Ваш отзыв будет рассмотрен в приоритетном порядке."
    else:
        message = f"Спасибо, {feedback.name}! Ваш отзыв сохранён."

    return { "message": message }


@app.get("/comments")
async def read_feedbacks():
    return feedbacks