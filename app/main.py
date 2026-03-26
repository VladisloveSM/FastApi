from fastapi import FastAPI, Depends, HTTPException, status
from app.models import Feedback, User, UserLogin, Data
from app.config import load_config
from app.security import create_jwt_token, get_current_user
from app.db import USERS_DATA, RESOURCE
from passlib.context import CryptContext
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.rbac import PermissionChecker

app = FastAPI()
# Set Config
config = load_config()

# Set Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

#Set hash metod
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

feedbacks = []

@app.post("/login")
async def login(user_in: UserLogin):
    for user in USERS_DATA:
        if user["username"] == user_in.username and user["password"] == user_in.password:
            # Generate a JWT token for the user
            token = create_jwt_token({"sub": user_in.username})
            return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid data request")


@app.get("/create")
@PermissionChecker(["admin", "user"])
async def create_resource(data: Data, current_user: User = Depends(get_current_user)):
    """Create a resource with the provided data"""
    RESOURCE[data.id] = {"id": data.id, "data": data.data}
    return {"id": data.id, "data": data.data}

@app.get("/admin")
@PermissionChecker(["admin"])
async def admin_info(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}! Welcome to the admin page."}

@app.get("/user")
@PermissionChecker(["user"])
async def user_info(current_user: User = Depends(get_current_user)):
    """Route for users"""
    return {"message": f"Hello, {current_user.username}! Welcome to the user page."}

@app.get("/about_me")
async def about_me(current_user: User = Depends(get_current_user)):
    """Information about the current user"""
    return current_user



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
