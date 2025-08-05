from fastapi import FastAPI

my_api = FastAPI()

@my_api.get("/")
async def root():
    return {"message": "Авторелоад действительно работает!"}