import re

ban_words = ["редиск", "бяк", "козявк"]

def verify_user_agent(user_agent: str):
    if user_agent is None or user_agent.strip() == "":
        return False
    return True

def varify_accept_language(accept_language: str):
    if accept_language is None or accept_language.strip() == "":
        return False
    
    pattern = r'^[a-zA-Z]{2}(-[a-zA-Z]{2})?(;q=[0-9]\.?[0-9]?)?(,\s*[a-zA-Z]{2}(-[a-zA-Z]{2})?(;q=[0-9]\.?[0-9]?)?)*$'

    if not re.match(pattern, accept_language):
        return False

    return True

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