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

# Обрабатываем GET-запрос, чтобы вернуть список пользователей 
@app.get("/users")
async def read_users(username: str = None, email: str = None, limit: int = 10):
    return fake_db

@app.post("/add_user", response_model=User)
async def create_user(user: User):
    fake_db.append({
        "username": user.username,
        "user_info": user.user_info
    })
    return user