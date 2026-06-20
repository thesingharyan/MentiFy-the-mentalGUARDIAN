import json
from google import genai

from config import GOOGLE_API_KEY

client = genai.Client(api_key=GOOGLE_API_KEY)


def generate_insights(answers, prediction, confidence, probabilities):
    prompt = f"""
You are Mentify AI, a mental wellness assistant.

The following prediction was produced by a machine learning model.

Prediction:
{prediction}

Confidence:
{confidence}

Class Probabilities:
{json.dumps(probabilities, indent=2)}

User Responses:
{json.dumps(answers, indent=2)}

Your task:
Analyze the user's responses together with the ML prediction.

Return ONLY valid JSON.

The JSON format MUST be:

{{
    "summary": "...",

    "possible_causes": [
        "...",
        "..."
    ],

    "recommendations": [
        "...",
        "...",
        "..."
    ],

    "daily_habits": [
        "...",
        "..."
    ],

    "professional_help": true,

    "disclaimer": "This is not a medical diagnosis. If symptoms are severe or persistent, consult a qualified mental health professional."
}}

Rules:
- Do not diagnose medical conditions.
- Be supportive and empathetic.
- Base your response on BOTH the prediction and the user's responses.
- Recommend professional help only when appropriate based on the information provided.
- Return ONLY JSON.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove Markdown code fences if Gemini adds them
    if text.startswith("```json"):
        text = text[len("```json"):]

    if text.startswith("```"):
        text = text[len("```"):]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    return json.loads(text)