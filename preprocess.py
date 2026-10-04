# preprocess.py
import re

def clean_text(text: str) -> str:
    """
    Clean and preprocess text for ML model
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    
    # Remove special characters but keep spaces
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text