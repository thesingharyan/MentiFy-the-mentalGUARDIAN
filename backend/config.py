import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file automatically

MODEL_PATH = "./model"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

LABELS = [
    "Anxiety",
    "Bipolar",
    "Depression",
    "Normal",
    "Personality disorder",
    "Stress",
    "Suicidal"
]