import re
from app.constants import KNOWN_MERCHANTS
    

    
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_merchant(text):
    merchant=text.lower()
    for keyword in KNOWN_MERCHANTS:
        if keyword in merchant:
            return keyword
    return None
        