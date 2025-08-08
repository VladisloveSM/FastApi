from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import Request

app = FastAPI()

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.post("/calculate")
async def calculate(request: Request):
    data = await request.json()
    num1 = data.get("num1")
    num2 = data.get("num2")
    return {"result": num1 + num2}