from pydantic import BaseModel
from pydantic import BaseModel, Field

class User(BaseModel):
    age: int
    name: str

class Feedback(BaseModel):
    name: str = Field(max_length=50)
    message: str = Field(max_length=50)