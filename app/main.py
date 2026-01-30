from fastapi import FastAPI, Cookie, HTTPException, Response, Depends, Header
from app.models import Feedback, LoginData
from typing import Optional
from datetime import datetime, timezone
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer  
import uuid

app = FastAPI() 

feedbacks = []

COOKIE_LIFETIME = 300  # 5 minutes in seconds
REFRESH_TIME = 180 # 3 minutes in seconds
SECRET_KEY = 'supersecretkey'
serializer = URLSafeTimedSerializer(SECRET_KEY)

users = [
    {"id": str(uuid.uuid4()), "username": "admin", "password": "secret"},
    {"id": str(uuid.uuid4()), "username": "user", "password": "password123"},
    {"id": str(uuid.uuid4()), "username": "user123", "password": "password123"},
]


def verify_session(session_token: Optional[str] = Cookie(None)):
    if session_token is None:
        raise HTTPException(status_code=401, detail="Cookie not found")
    try:
        unsigned = serializer.loads(session_token, max_age=COOKIE_LIFETIME)
    except SignatureExpired:
        raise HTTPException(status_code=401, detail="Session expired")
    except BadSignature:
        raise HTTPException(status_code=401, detail="Invalid session")

    return session_token


def refresh_token(session_token: str):
    data, timestamp = serializer.loads(session_token, max_age=COOKIE_LIFETIME, return_timestamp=True)
    age_seconds = (datetime.now(timezone.utc) - timestamp).total_seconds()

    if age_seconds >= REFRESH_TIME:
        new_token = serializer.dumps(data)
        return new_token
    else:
        return None


@app.post("/login")
async def login(data: LoginData, response: Response):
    user = next(
        (u for u in users if u["username"] == data.username and u["password"] == data.password),
        None
    )
    
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    # Создаём токен
    signature = serializer.dumps(user["id"])
    
    # Устанавливаем cookie (перезапишет если была)
    response.set_cookie(
        key="session_token",
        value=signature,
        httponly=True,
        secure=False,
        max_age=COOKIE_LIFETIME,
        samesite="lax"
    )

    return {"message": f"Successful login. Your cookie: {signature}"}


@app.get("/profile")
async def get_user(session_token: str = Depends(verify_session), response: Response = None):
    new_token = refresh_token(session_token)
    if new_token:
        response.set_cookie(
            key="session_token",
            value=new_token,
            httponly=True,
            secure=False,
            max_age=COOKIE_LIFETIME,
            samesite="lax"
        )
        return {"message": f"User your new session: {new_token}"}
    else:
        return {"message": f"You don't need to refresh your session: {session_token}"}


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