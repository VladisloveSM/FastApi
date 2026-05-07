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

# Set hash metod
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

feedbacks = []

@app.post("/create")
async def register(todo: Todo):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        
        cursor.execute(
            "INSERT INTO todo (title, description) VALUES (?, ?)",
            (todo.title, todo.description)
        )
        
        conn.commit()
        todo_id = cursor.lastrowid
        
        return {
            "id": todo_id,
            "title": todo.title,
            "description": todo.description,
            "completed": False
        }
            
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create todo: {str(e)}"
        )
    
    finally:
        conn.close()
    

@app.get("/todo/{todo_id}")
async def get_todo(todo_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM todo WHERE id = ?", (todo_id,))
        todo = cursor.fetchone()
        
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        
        return {
            "id": todo[0],
            "title": todo[1],
            "description": todo[2],
            "completed": todo[3]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create todo: {str(e)}"
        )
    
    finally:
        conn.close()


@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo: Todo):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "UPDATE todo SET title = ?, description = ?, completed = ? WHERE id = ?",
            (todo.title, todo.description, todo.completed, todo_id)
        )
        
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        
        conn.commit()
        
        return {
            "id": todo_id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update todo: {str(e)}"
        )
    
    finally:
        conn.close()

@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM todo WHERE id = ?", (todo_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        
        conn.commit()
        
        return {"message": "Todo deleted successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete todo: {str(e)}"
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
