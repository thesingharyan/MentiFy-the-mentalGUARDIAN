import json
from google import genai

from config import GOOGLE_API_KEY

client = genai.Client(api_key=GOOGLE_API_KEY)


def generate_insights(
    answers,
    overall_prediction,
    question_predictions
):
    """
    Generates personalized mental wellness insights using:
    - Overall majority-vote prediction
    - Individual predictions for each answer
    - User responses
    """

    formatted_predictions = ""

    for item in question_predictions:
        formatted_predictions += f"""
Question: {item['question']}

Prediction: {item['prediction']}
Confidence: {item['confidence']}

Answer:
{item['answer']}

------------------------
"""

    answers_text = "\n".join([
        f"{item['question']} {item['answer']}" for item in answers
    ])

    prompt = f"""
You are Mentify AI, a supportive mental wellness assistant.

IMPORTANT RULES:
- You are NOT a doctor.
- Never diagnose any medical condition.
- Do not claim certainty about mental illness.
- Be supportive, calm, and non-alarming.
- Use the model output only as a reference, not a diagnosis.
- If risk is high (Suicidal), respond with urgency but stay calm and supportive.

OVERALL PREDICTION:
{overall_prediction}

QUESTION-WISE ANALYSIS:
{formatted_predictions}

ALL USER ANSWERS TEXT:
{answers_text}

ALL USER ANSWERS JSON:
{json.dumps(answers, indent=2)}

Your task:
Analyze the user's mental state based on:
1. Their answers
2. Pattern across responses
3. Model predictions (secondary signal)

Generate ONLY valid JSON in this format:

{{
    "summary": "",

    "possible_causes": [
        "",
        ""
    ],

    "recommendations": [
        "",
        "",
        ""
    ],

    "daily_habits": [
        "",
        "",
        "",
        ""
    ],

    "professional_help": false,

    "risk_level": "low",

    "final_label": "",

    "disclaimer": "This is not a medical diagnosis. If you are struggling, consider speaking to a qualified mental health professional."
}}

RISK LEVEL RULES:

- Normal → low
- Stress → low or medium
- Anxiety → medium
- Bipolar → medium
- Depression → medium
- Personality disorder → medium
- Suicidal → high

GUIDELINES:
- Focus more on USER ANSWERS than model labels
- Keep tone empathetic and supportive
- Avoid fear-based language
- Give practical suggestions
- Be concise but meaningful
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # clean markdown if Gemini returns ```json
    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()
    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    return json.loads(text)