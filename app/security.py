import datetime
import jwt
from app.db import get_user
from app.models import User
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, Request, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Should kepp in the .env
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Authorization error")

def get_user_from_token(token: str = Depends(oauth2_scheme)) -> str:
    return decode_token(token)

def username_from_request(request: Request) -> str:
    auth = request.headers.get("authorization", "")
    prefix = "bearer "
    if not auth.lower().startswith(prefix):
        return "anonymous"
    token = auth[len(prefix):].strip()
    try:
        return decode_token(token)
    except HTTPException:
        return "anonymous"

def get_current_user(current_username: str = Depends(get_user_from_token)) -> User:
    """Get the current user based on their username from the token"""
    user = get_user(current_username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def get_rate_limit_by_role(request: Request) -> str:
    username = username_from_request(request)
    user = get_user(username) if username != "anonymous" else None
    roles = user.roles if user else []
    
    if "admin" in roles:
        return "1000/minute"
    elif "user" in roles:
        return "20/minute"
    elif "guest" in roles:
        return "5/minute"
    return "1/minute"