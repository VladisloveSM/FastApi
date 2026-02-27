from fastapi import FastAPI, Depends
from app.models import Feedback, User
from app.config import load_config
from passlib.context import CryptContext
from app.db import get_user, USERS_DATA
from security import create_jwt_token, get_user_from_token

app = FastAPI()

config = load_config()

feedbacks = []

@app.post("/login")
async def login(user_in: User): 
    for user in USERS_DATA:
        if user.get("username") == user_in.username and user.get("password") == user_in.password:
            # If the verification is successful, generate a token for the user
            token = create_jwt_token({"sub": user_in.username})  # 'sub' stands for subject, in our case the user's name
            return {"access_token": token, "token_type": "bearer"}
    return {"error": "Invalid credentials"}


# Secure route that returns user information
@app.get("/about_me")
async def about_me(current_user: str = Depends(get_user_from_token)):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы возвращаем информацию о пользователе.
    """
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
