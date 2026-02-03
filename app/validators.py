import re
from fastapi import HTTPException

ban_words = ["редиск", "бяк", "козявк"]
MINIMUM_APP_VERSION = "0.0.2"
MINIMUM_VERSION_VECTOR = tuple(map(int, MINIMUM_APP_VERSION.split('.')))

def verify_user_agent(user_agent: str):
    if user_agent is None or user_agent.strip() == "":
        raise HTTPException(status_code=400, detail=f"Invalid request.")
    return user_agent

def varify_accept_language(accept_language: str):
    if accept_language is None or accept_language.strip() == "":
        raise HTTPException(status_code=400, detail=f"Invalid request.")
    
    pattern = r'^[a-zA-Z]{2}(-[a-zA-Z]{2})?(;q=[0-9]\.?[0-9]?)?(,\s*[a-zA-Z]{2}(-[a-zA-Z]{2})?(;q=[0-9]\.?[0-9]?)?)*$'

    if not re.match(pattern, accept_language):
        raise HTTPException(status_code=400, detail=f"Invalid request.")

    return accept_language

def verify_x_current_version(x_current_version: str):
    if x_current_version is None or x_current_version.strip() == "":
        raise HTTPException(status_code=400, detail=f"Invalid request.")
    
    pattern = r'^\d+\.\d+\.\d+$'

    if not re.match(pattern, x_current_version):
        raise HTTPException(status_code=400, detail=f"Invalid request.")
    
    input_value = tuple(map(int, x_current_version.split('.')))

    if input_value < MINIMUM_VERSION_VECTOR:
        raise HTTPException(status_code=422, detail=f"Need to update app.")

    return x_current_version

def validate_feedback(message: str) -> bool:
    text = message
    for ban in ban_words:
        pattern = r"\b" + re.escape(ban.lower())
        if re.search(pattern, text, flags=re.IGNORECASE | re.UNICODE):
            return False
    return True

def validate_phone(phone: str | None) -> bool:
    if phone is None:
        return True
    return phone.isdigit()