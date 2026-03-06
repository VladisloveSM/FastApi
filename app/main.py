from fastapi import FastAPI, Depends, HTTPException
from app.models import Feedback, User
from app.config import load_config
from passlib.context import CryptContext
from app.db import get_user, USERS_DATA
from app.security import create_jwt_token, get_user_from_token
import secrets

app = FastAPI()

config = load_config()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

feedbacks = []

@app.post("/register")
async def register(user: User):
    for existing_user in USERS_DATA:
        if secrets.compare_digest(existing_user.get("username").encode("utf-8"), user.username.encode("utf-8")):
            raise HTTPException(status_code=409, detail="User already exists")
    USERS_DATA.append({"username": user.username, "password": pwd_context.hash(user.password)})
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user_in: User): 
    user = get_user(user_in.username)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not CryptContext(schemes=["bcrypt"], deprecated="auto").verify(user_in.password, user.get("password")):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_jwt_token({"sub": user_in.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Secure route that returns user information
@app.get("/protected_resource")
async def about_me(current_user: str = Depends(get_user_from_token)):
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
