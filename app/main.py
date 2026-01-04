from fastapi import FastAPI 
from pydantic import BaseModel

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