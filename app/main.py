from datetime import datetime
from fastapi import FastAPI, Cookie, HTTPException, Response, Depends, Header
from app.models import Feedback, CommonHeaders

app = FastAPI() 

feedbacks = []

@app.get("/headers")
async def read_headers(headers: CommonHeaders = Depends(CommonHeaders.get_common_headers)):
    return { "User-Agent": headers.user_agent, "Accept-Language": headers.accept_language, "X-Current-Version": headers.x_current_version }

@app.get("/info")
async def set_cookie(response: Response, headers: CommonHeaders = Depends(CommonHeaders.get_common_headers)):
    response.headers["X-Server-Time"] = datetime.utcnow().isoformat()
    return {    
                "Message": "Welcome, your headers successfully handled.",
                "headers": {
                    "User-Agent": headers.user_agent, 
                    "Accept-Language": headers.accept_language
                }
            }

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