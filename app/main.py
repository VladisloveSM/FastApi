from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from app.models import Feedback, User, UserInDB
from app.config import load_config
from passlib.context import CryptContext
import secrets

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,   
)

security = HTTPBasic()
security_docs = HTTPBasic()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config = load_config()

fake_users_db = {
    "admin": UserInDB(
        username="admin", 
        hashed_password=pwd_context.hash("secretpassw")
    ),
    "user": UserInDB(
        username="user", 
        hashed_password=pwd_context.hash("userpass123")
    )
}

feedbacks = []

def verify_docs_credentials(
    credentials: HTTPBasicCredentials = Depends(security_docs)
):
    correct_username = secrets.compare_digest(
        credentials.username,
        config.docs.user
    )
    correct_password = secrets.compare_digest(
        credentials.password,
        config.docs.password
    )

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username

def auth_user(credentials: HTTPBasicCredentials = Depends(security)):

    user = fake_users_db.get(credentials.username)
    
    if user is None or not secrets.compare_digest(user.username, credentials.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    password_correct = pwd_context.verify(
        credentials.password, 
        user.hashed_password
    )
    
    if not password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return user

if config.mode == "DEV":
    @app.get("/docs", include_in_schema=False)
    async def get_swagger_docs(
        username: str = Depends(verify_docs_credentials)
    ):
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title="API Docs"
        )

    @app.get("/openapi.json", include_in_schema=False)
    async def get_openapi_schema(
        username: str = Depends(verify_docs_credentials)
    ):
        return get_openapi(
            title=app.title,
            version=app.version,
            routes=app.routes,
        )

@app.get("/config")
async def read_config():
    return {"mode": f"{config.mode}"}

@app.post("/register")
async def register(user: User):
    fake_users_db[user.username] = UserInDB(username=user.username, hashed_password=pwd_context.hash(user.password))
    return {"message": f"User {user.username} registered successfully!"}

@app.get("/login")
async def read_users(user = Depends(auth_user)):
    return {"message": f"Welcome, {user.username}!"}


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
