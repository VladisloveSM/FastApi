from pydantic import BaseModel, Field, field_validator, EmailStr
import validators

class User(BaseModel):
    age: int
    name: str


class Contact(BaseModel):
    email: EmailStr
    phone: str = Field(min_length=7, max_length=15)

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