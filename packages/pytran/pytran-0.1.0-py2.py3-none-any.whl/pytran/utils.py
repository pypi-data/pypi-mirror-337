import re

def clean_text(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\s]", "", text).strip()