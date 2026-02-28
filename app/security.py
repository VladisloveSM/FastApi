import jwt
import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Dict

# OAuth2PasswordBearer extracts the token from the header "Authorization: Bearer <token>"
# The tokenUrl parameter specifies the route by which clients can obtain a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "mysecretkey"  # In real practice, generate a key, for example, using “openssl rand -hex 32”, and store it securely.
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Timelife of token

# Function for creating a JWT token with a specified lifetime
def create_jwt_token(data: Dict):
    to_encode = data.copy()  # Copy the data so as not to change the original dictionary.
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Set the token expiry time
    to_encode.update({"exp": expire})  # Add the expiry time to the token data
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encrypt the token using a secret key and algorithm

# Функция для получения пользователя из токена
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode the token using the secret key
        return payload.get("sub")  # Return the user (subject) statement from the payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")  # Handling token expiry errors
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")  # Handling invalid token error