from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi_limiter.depends import RateLimiter
from app.models import Feedback, User, UserLogin, Data
from app.config import load_config
from app.security import create_jwt_token, get_current_user, get_rate_limit_by_role, username_from_request
from app.db import USERS_DATA, RESOURCE, get_user
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

#Set hash metod
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

feedbacks = []

@app.post("/login")
async def login(user_in: UserLogin):
    for user in USERS_DATA:
        if user["username"] == user_in.username and user["password"] == user_in.password:
            # Generate a JWT token for the user
            token = create_jwt_token({"sub": user_in.username})
            return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid data request")


@app.post("/protected_resources/{username}")
@PermissionChecker(["admin", "user", "guest"])
@limiter.limit(get_rate_limit_by_role, key_func=username_from_request)
async def create_resource(resource: Data, request: Request, current_user: User = Depends(get_current_user), username: str = None):
    RESOURCE[username] = resource
    return {"message": "Resource created successfully"}

@app.get("/protected_resources/{username}")
@PermissionChecker(["admin", "user", "guest"])
@limiter.limit(get_rate_limit_by_role, key_func=username_from_request)
async def get_resource(request: Request, current_user: User = Depends(get_current_user), username: str = None):
    if username not in RESOURCE:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return RESOURCE[username]

@app.put("/protected_resources/{username}")
@PermissionChecker(["admin", "user", "guest"])
@limiter.limit(get_rate_limit_by_role, key_func=username_from_request)
async def update_resource(resource: Data, request: Request, current_user: User = Depends(get_current_user), username: str = None):
    if username not in RESOURCE:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    RESOURCE[username] = resource
    return {"message": "Resource updated successfully"}

@app.delete("/protected_resources/{username}")
@PermissionChecker(["admin", "user", "guest"])
@limiter.limit(get_rate_limit_by_role, key_func=username_from_request)
async def delete_resource(request: Request, current_user: User = Depends(get_current_user), username: str = None):
    if username not in RESOURCE:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    del RESOURCE[username]
    return {"message": "Resource deleted successfully"}


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
