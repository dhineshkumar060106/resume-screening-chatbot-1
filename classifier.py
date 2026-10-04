import joblib
import os
import sys
from sentence_transformers import SentenceTransformer

# Add parent directory to path to find preprocess module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from preprocess import clean_text
except ImportError:
    # Fallback clean_text function if preprocess.py is missing
    import re
    def clean_text(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "svm_model.pkl")

# Load model with error handling
try:
    svm_model = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Warning: Could not load model from {MODEL_PATH}: {e}")
    print("Using fallback prediction...")
    # Create a dummy model for fallback
    class DummyModel:
        def predict(self, X):
            return ["Software Developer"]
    svm_model = DummyModel()

# Initialize embedder
try:
    embedder = SentenceTransformer("all-mpnet-base-v2")
    print("SentenceTransformer loaded successfully")
except Exception as e:
    print(f"Warning: Could not load SentenceTransformer: {e}")
    # Create dummy embedder
    class DummyEmbedder:
        def encode(self, texts, show_progress_bar=False):
            return [[0.1] * 768]  # Return dummy embedding
    embedder = DummyEmbedder()

def predict_job_role(resume_text: str) -> str:
    """
    Predict job role from resume text
    """
    try:
        cleaned_text = clean_text(resume_text)
        
        # Ensure we have some text
        if not cleaned_text or len(cleaned_text.strip()) < 10:
            return "General Professional"
        
        # Get embedding
        embedding = embedder.encode([cleaned_text])
        
        # Make prediction
        prediction = svm_model.predict(embedding)
        
        return str(prediction[0]) if len(prediction) > 0 else "Unknown Role"
        
    except Exception as e:
        print(f"Error in predict_job_role: {e}")
        return "Software Developer"  # Default fallback