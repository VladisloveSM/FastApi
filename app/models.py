from pydantic import BaseModel, Field, field_validator
import validators

class User(BaseModel):
    age: int
    name: str

class Feedback(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=10, max_length=500)

    @field_validator('message')
    def check_message(cls, value) -> str:
        if not validators.validate_feedback(value):
            raise ValueError("Использование недопустимых слов!")
        return value