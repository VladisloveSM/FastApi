from fastapi import FastAPI, Cookie, HTTPException, Response, Depends
from app.models import Feedback, LoginData
from typing import Optional
from datetime import datetime, timedelta
import uuid

app = FastAPI() 

feedbacks = []

users = [
    {"username": "admin", "password": "secret"},
    {"username": "user", "password": "password123"},
    {"username": "user123", "password": "password123"},
]

valid_sessions = {}

def verify_session(session_token: Optional[str] = Cookie(None)):
    if session_token is None:
        raise HTTPException(status_code=401, detail="Cookie не найдена")
    
    if session_token not in valid_sessions:
        raise HTTPException(status_code=401, detail=f"Невалидная сессия {session_token}")
    
    if valid_sessions[session_token]["expiration"] < datetime.now():
        del valid_sessions[session_token]
        raise HTTPException(status_code=401, detail="Сессия истекла")
    
    return session_token


@app.post("/login")
async def login(data: LoginData, response: Response):
    for user in users:
        if user["username"] == data.username and user["password"] == data.password:
            id = uuid.uuid4()
            response.set_cookie(
                key="session_token",
                value=id,
                httponly=True,
                secure=False,  # True для HTTPS
                samesite="lax"
            )
            valid_sessions[str(id)] =  { "username": data.username, "expiration": datetime.now() + timedelta(hours=1) }
            return {"message": f"Успешный вход, и вот моя сессия: {id}"}
    return {"message": "Неверные учетные данные."}


@app.get("/user")
async def get_user(session_token: str = Depends(verify_session)):
    user_info = valid_sessions.get(session_token)
    return {"username": user_info["username"]}


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