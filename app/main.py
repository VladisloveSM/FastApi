import re
from fastapi import FastAPI, Cookie, HTTPException, Response, Depends, Header
from app.models import Feedback, CommonHeaders

app = FastAPI() 

feedbacks = []

@app.get("/headers")
async def read_headers(headers: CommonHeaders = Depends(CommonHeaders.get_common_headers)):
    return { "User-Agent": headers.user_agent, "Accept-Language": headers.accept_language }


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