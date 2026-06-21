import os
from dotenv import load_dotenv

load_dotenv()

# Hugging Face model path (your uploaded model repo)
HF_MODEL = os.getenv("HF_MODEL")

# Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Flask environment
FLASK_ENV = os.getenv("FLASK_ENV", "development")

# Model settings
MAX_LENGTH = 256

# Labels MUST match training order
LABELS = [
    "Anxiety",
    "Bipolar",
    "Depression",
    "Normal",
    "Personality Disorder",
    "Stress",
    "Suicidal"
]