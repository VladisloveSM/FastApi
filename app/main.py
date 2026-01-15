from fastapi import FastAPI 
from app.models import Feedback, User

app = FastAPI() 

fake_db = [ 
{
    "age": 12,
    "name": "love cyberpunk"
}, 
{
    "age": 34,
    "name": "love sci-fi"
} 
]

feedbacks = []

@app.get("/users/{user_name}")
async def read_user(user_name: str):
    for user in fake_db:
        if user["name"] == user_name:
            return user
    return {"error": "User not found"}


@app.get("/users")
async def read_users(limit: int = 10):
    return fake_db[:limit]

@app.post("/add_user", response_model=User)
async def create_user(user: User):
    fake_db.append({
        "name": user.name,
        "age": user.age
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