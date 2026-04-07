from fastapi import FastAPI, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from app.models import Feedback, User, UserLogin, Data
from app.config import load_config
from app.security import create_jwt_token, get_current_user
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
# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

#Set hash metod
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

feedbacks = []


def get_rate_limit_by_role(user=Depends(get_current_user)):
    if 'admin' in user.roles:
        return RateLimiter(times=1000, seconds=60)
    elif 'premium' in user.roles:
        return RateLimiter(times=20, seconds=60)
    elif 'guest' in user.roles:
        return RateLimiter(times=5, seconds=60)
    else:
        return RateLimiter(times=1, seconds=60)


@app.post("/login")
async def login(user_in: UserLogin):
    for user in USERS_DATA:
        if user["username"] == user_in.username and user["password"] == user_in.password:
            # Generate a JWT token for the user
            token = create_jwt_token({"sub": user_in.username})
            return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid data request")


@app.post("/create_resource")
@PermissionChecker(["admin"])
async def create_resource(data: Data, limiter=Depends(get_rate_limit_by_role)):
    """Create a resource with the provided data"""
    if data.id in RESOURCE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource already exists")
    RESOURCE[data.id] = data.data
    return {"id": data.id, "data": data.data}


@app.post("/edit_resource")
@PermissionChecker(["admin", "user"])
async def edit_resource(data: Data, limiter=Depends(get_rate_limit_by_role)):
    """Edit a resource with the provided data"""
    if RESOURCE.get(data.id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    RESOURCE[data.id] = data.data
    return {"id": data.id, "data": data.data}


@app.get("/resources")
@PermissionChecker(["admin", "user", "guest"])
async def get_resource(limiter=Depends(get_rate_limit_by_role)):
    return RESOURCE

@app.get("/protected_procedure")
@PermissionChecker(["admin", "user"])
async def protected_procedure(limiter=Depends(get_rate_limit_by_role)):
    return {"message": "This is a protected procedure"}



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
