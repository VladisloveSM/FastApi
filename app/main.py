from fastapi import FastAPI, Cookie, HTTPException, Response, Depends
from app.models import Feedback, LoginData
from typing import Optional
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import uuid

app = FastAPI() 

feedbacks = []

SECRET_KEY = 'supersecretkey'
serializer = URLSafeTimedSerializer(SECRET_KEY)

users = [
    {"id": str(uuid.uuid4()), "username": "admin", "password": "secret"},
    {"id": str(uuid.uuid4()), "username": "user", "password": "password123"},
    {"id": str(uuid.uuid4()), "username": "user123", "password": "password123"},
]

valid_sessions = {}

def verify_session(session_token: Optional[str] = Cookie(None)):
    if session_token is None:
        raise HTTPException(status_code=401, detail="Cookie не найдена")
    user_id, signature = session_token.split(".", 1)
    data = serializer.loads(signature, max_age=3600)

    if user_id != data:
        raise HTTPException(status_code=401, detail="Недействительная сессия")
    
    return session_token


@app.post("/login")
async def login(data: LoginData, response: Response):
    for user in users:
        if user["username"] == data.username and user["password"] == data.password:
            signature = serializer.dumps(user['id'])
            response.set_cookie(
                key="session_token",
                value=f"{user['id']}.{signature}",
                httponly=True,
                max_age=3600,
                secure=False,  # True для HTTPS
                samesite="lax"
            )
            return {"message": f"Успешный вход, и вот моя сессия: {user['id']}.{signature}"}
    return {"message": "Неверные учетные данные."}


@app.get("/profile")
async def get_user(session_token: str = Depends(verify_session)):
    user_id, signature = session_token.split(".", 1)
    return {"message": f"Пользователь с ID: {user_id}, Сигнатура: {signature}"}


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