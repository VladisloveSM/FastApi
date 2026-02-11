from datetime import datetime
from fastapi import FastAPI, Response, Depends, HTTPException
from app.models import Feedback, User

app = FastAPI() 

users = [
    { "username": "admin", "password": "admin" },
    { "username": "user", "password": "user" },
    { "username": "guest", "password": "guest" }
]

feedbacks = []

def check_auth(username: str, password: str):
    user = next(
        (u for u in users if u["username"] == username and u["password"] == password),
        None
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return User(username=user["username"], password=user["password"])

@app.get("/login")
async def login(user: User = Depends(check_auth)):
    return { "username": user.username, "password": user.password }


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
