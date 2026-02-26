# db.py
# User database simulation

USERS_DATA = [
    {"username": "admin", "password": "adminpass"}  # In a real database, passwords should be stored as hashes.
]

def get_user(username: str):
    """
    Функция для поиска пользователя по имени пользователя. 
    В реальном проекте это должно быть запросом к базе данных.
    """
    for user in USERS_DATA:
        if user.get("username") == username:
            return user
    return None
