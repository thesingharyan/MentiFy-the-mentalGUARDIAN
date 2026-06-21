import json
from google import genai

from config import GOOGLE_API_KEY

client = genai.Client(api_key=GOOGLE_API_KEY)


def generate_insights(answers, prediction, confidence, probabilities):
    """
    Uses Gemini to generate mental health insights based on:
    - user answers
    - ML prediction
    - confidence scores
    """

    prompt = f"""
You are "Mentify AI", a supportive mental wellness assistant.

IMPORTANT RULES:
- You are NOT a medical professional.
- Do NOT diagnose medical conditions.
- Be empathetic and supportive.
- If risk seems high (like suicidal), recommend seeking immediate help.
- Keep language simple and non-judgmental.

INPUT DATA:

ML Prediction: {prediction}
Confidence: {confidence}

Class Probabilities:
{json.dumps(probabilities, indent=2)}

User Answers:
{json.dumps(answers, indent=2)}

TASK:
Generate a structured JSON response.

Return ONLY valid JSON in this format:

{{
    "summary": "...",
    "possible_causes": ["...", "..."],
    "recommendations": ["...", "...", "..."],
    "daily_habits": ["...", "..."],
    "professional_help": true,
    "risk_level": "low | medium | high",
    "disclaimer": "This is not a medical diagnosis. If you are struggling, consider speaking to a qualified mental health professional."
}}

GUIDELINES:
- If prediction is "Suicidal" → risk_level MUST be "high"
- If prediction is "Depression" or confidence > 0.85 → risk_level at least "medium"
- Otherwise mostly "low"
- recommendations should be practical and simple
- daily habits should be small daily actions
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Clean markdown if Gemini wraps response
    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()
    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    return json.loads(text)