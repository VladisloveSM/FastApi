from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi_limiter.depends import RateLimiter
from app.models import Feedback, Todo
from app.config import load_config
from passlib.context import CryptContext
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.database import get_db_connection

app = FastAPI()
# Set Config
config = load_config()

# Set Limiter
# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter

#Set hash metod
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

feedbacks = []

@app.post("/create")
async def register(todo: Todo):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        
        cursor.execute(
            "INSERT INTO todos (title, description) VALUES (?, ?)",
            (todo.title, todo.description)
        )
        
        conn.commit()
        
        return {"message": "Todo created successfully!"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create todo: {str(e)}"
        )
    
    finally:
        conn.close()
    

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
