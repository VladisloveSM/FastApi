import re

ban_words = ["редиск", "бяк", "козявк"]


def validate_feedback(message: str) -> bool:
    text = message
    for ban in ban_words:
        pattern = r"\b" + re.escape(ban.lower())
        if re.search(pattern, text, flags=re.IGNORECASE | re.UNICODE):
            return False
    return True