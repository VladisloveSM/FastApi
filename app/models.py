from pydantic import BaseModel
from pydantic import BaseModel, Field

class User(BaseModel):
    age: int
    name: str

class Feedback(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=10, max_length=500)