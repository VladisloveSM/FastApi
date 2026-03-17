import jwt
import datetime
from app.db import get_user
from app.models import User
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends

# We define the authentication scheme (OAuth2 with password)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "mysecretkey"  # Generate using `openssl rand -hex 32`
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15 

def create_jwt_token(data: dict):
    """Creating a JWT token with an expiry time"""
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str = Depends(oauth2_scheme)):
    """Get user information from the token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(current_username: str = Depends(get_user_from_token)) -> User:
    """Get the current user based on their username from the token"""
    user = get_user(current_username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user