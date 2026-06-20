import os
from dotenv import load_dotenv

load_dotenv()

HF_MODEL = os.getenv("HF_MODEL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
FLASK_ENV = os.getenv("FLASK_ENV", "development")

MAX_LENGTH = 256

LABELS = [
    "Anxiety",
    "Bipolar",
    "Depression",
    "Normal",
    "Personality Disorder",
    "Stress",
    "Suicidal"
]