from fastapi import FastAPI, Cookie, HTTPException, Response, Depends, Header
from app.models import Feedback
from typing import Dict, Optional

app = FastAPI() 

feedbacks = []

def verify_headers(user_agent: Optional[str] = Header(default=None), accept_language: Optional[str] = Header(default=None)) -> Dict[str, str]:
    valid = True
    if user_agent is None or user_agent.strip() == "":
        valid = False
    if accept_language is None or accept_language.strip() == "":
        valid = False
    if not valid:
        raise HTTPException(status_code=400, detail=f"Invalid request.")
    
    return { "User-Agent": user_agent, "Accept-Language": accept_language }
    


@app.get("/headers")
async def read_headers(headers: Dict[str, str] = Depends(verify_headers)):
    return headers


@app.post("/feedback")
async def create_feedback(feedback: Feedback, is_premium: bool = False):
    feedbacks.append(feedback)
    if is_premium:
        message = f"Thank you, {feedback.name}! Your feedback has been saved. Your feedback will be reviewed with priority."
    else:
        message = f"Thank you, {feedback.name}! Your feedback has been saved."
    return { "message": message }


@app.get("/comments")
async def read_feedbacks():
    return feedbacks