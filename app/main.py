# main.py
from fastapi import FastAPI 

app = FastAPI() 

fake_db = [{"username": "vasya", "user_info": "любит колбасу"}, {"username": "katya", "user_info": "любит петь"}] 

# Обрабатываем GET-запрос, чтобы вернуть список пользователей 
@app.get('/users') 
async def get_all_users(): 
    return fake_db 

# Обрабатываем POST-запрос, чтобы добавить нового пользователя 
@app.post('/add_user') 
async def add_user(username: str, user_info: str): 
    fake_db.append({"username": username, "user_info": user_info}) 
    return {"message": "Юзер успешно добавлен в базу данных"}