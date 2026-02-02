from fastapi import HTTPException, Header
from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
import app.validators as validators


class CommonHeaders(BaseModel):
    user_agent: str
    accept_language: str

    @field_validator('user_agent')
    def verify_user_agent(cls, value) -> bool:
        if not validators.verify_user_agent(value):
            raise HTTPException(status_code=400, detail=f"Invalid request.")
        return value

    @field_validator('accept_language')
    def verify_accept_language(cls, value) -> bool:
        if not validators.varify_accept_language(value):
            raise HTTPException(status_code=400, detail=f"Invalid request.")
        return value
    

    def get_common_headers(
        user_agent: Optional[str] = Header(None, alias="User-Agent"),
        accept_language: Optional[str] = Header(None, alias="Accept-Language")
    ):
        return CommonHeaders(
            user_agent=user_agent,
            accept_language=accept_language
        )


class LoginData(BaseModel):
    username: str
    password: str


class Contact(BaseModel):
    email: EmailStr
    phone: Optional[str] = Field(default=None, min_length=7, max_length=15)

    @field_validator('phone')
    def check_phone(cls, value) -> str:
        if not validators.validate_phone(value):
            raise ValueError("Номер телефона должен содержать только цифры!")
        return value


class Feedback(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=10, max_length=500)

    contact: Contact

    @field_validator('message')
    def check_message(cls, value) -> str:
        if not validators.validate_feedback(value):
            raise ValueError("Использование недопустимых слов!")
        return value