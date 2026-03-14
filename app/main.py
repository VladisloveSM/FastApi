from fastapi import FastAPI, Depends, HTTPException, Request
from app.models import Feedback, User, UserToken
from app.config import load_config
from passlib.context import CryptContext
from app.db import get_user, refresh_tokens
from app.security import create_jwt_token, get_user_from_refresh_token
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

config = load_config()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

feedbacks = []

@app.post("/login")
async def login(user_in: User): 
    result = get_user(user_in.username, user_in.password)
    access_token, refresh_token = create_jwt_token({"sub": user_in.username})
    refresh_tokens[user_in.username] = refresh_token
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.post("/refresh")
@limiter.limit("5/minute")
async def refresh_token(user: UserToken, request: Request):
    if refresh_tokens.get(user.username) != user.refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    result = get_user_from_refresh_token(user.refresh_token)
    if result != user.username:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    access_token, refresh_token = create_jwt_token({"sub": user.username})
    refresh_tokens[user.username] = refresh_token
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# Secure route that returns user information
@app.get("/protected_resource")
async def about_me(current_user: str):
    user = get_user(current_user)
    if user:
        return user
    
    return {"error": "User not found"}


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
