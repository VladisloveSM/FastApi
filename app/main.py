from fastapi import FastAPI 
from pydantic import BaseModel
from models import Feedback

app = FastAPI() 

class User(BaseModel):
    username: str
    user_info: str

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

fake_db_feedback = []

ban_words = ["редиск", "бяк", "козявк"]

async def validate_feedback(message: str) -> bool:
    words = message.lower().split()
    for ban_word in ban_words:
        if any(ban_word.lower() in s for s in words):
            return False
    return True

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

@app.post("/add_feedback")
async def create_feedback(feedback: Feedback):
    fake_db_feedback.append({
        "name": feedback.name,
        "comments": feedback.message
    })
    return {"message": f"Feedback received. Thank you, {feedback.name}!"}

@app.get("/comments")
async def read_feedbacks():
    return fake_db_feedback