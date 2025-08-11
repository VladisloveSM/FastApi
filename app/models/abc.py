from datetime import date
from pydantic import BaseModel

# Функция с аннотацией типа параметра, что позволяет получать поддержку проверки типов в IDE
def main(user_id: str):
    return user_id

# Еще один пример создания модели Pydantic
class User(BaseModel):
    id: int
    name: str
    joined: date

# Модель User может быть использована для создания объектов и распаковки JSON-запросов:
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)