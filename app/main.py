from fastapi import FastAPI 
from app.models import Feedback, User

app = FastAPI() 

fake_db = [ 
{
    "username": "vlad",
    "user_info": "love cyberpunk"
}, 
{
    "username": "anton",
    "user_info": "love sci-fi"
} 
]

feedbacks = []

@app.get("/users/{user_name}")
async def read_user(user_name: str):
    for user in fake_db:
        if user["username"] == user_name:
            return user
    return {"error": "User not found"}


@app.get("/users")
async def read_users(limit: int = 10):
    return fake_db[:limit]

@app.post("/add_user", response_model=User)
async def create_user(user: User):
    fake_db.append({
        "username": user.username,
        "user_info": user.user_info
    })
    return user

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