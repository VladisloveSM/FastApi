import re
from fastapi import FastAPI, Cookie, HTTPException, Response, Depends, Header
from app.models import Feedback
from typing import Dict, Optional

app = FastAPI() 

feedbacks = []

def verify_user_agent(user_agent: Optional[str] = Header(default=None)):
    if user_agent is None or user_agent.strip() == "":
        raise HTTPException(status_code=400, detail=f"Invalid request.")
    return user_agent

def varify_accept_language(accept_language: Optional[str] = Header(default=None)):
    if accept_language is None or accept_language.strip() == "":
        raise HTTPException(status_code=400, detail=f"Invalid request.")
    
    pattern = r'^[a-zA-Z]{2}(-[a-zA-Z]{2})?(;q=[0-9]\.?[0-9]?)?(,\s*[a-zA-Z]{2}(-[a-zA-Z]{2})?(;q=[0-9]\.?[0-9]?)?)*$'

    if not re.match(pattern, accept_language):
        raise HTTPException(status_code=400, detail=f"Invalid request.")

    return accept_language


@app.get("/headers")
async def read_headers(user_agent: str = Depends(verify_user_agent), accept_language: str = Depends(varify_accept_language)):
    return { "User-Agent": user_agent, "Accept-Language": accept_language }


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