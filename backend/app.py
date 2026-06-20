from flask import Flask, request, jsonify
from flask_cors import CORS

from predictor import predict
from llm import generate_insights

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Mentify Backend Running!"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON received."
        }), 400

    answers = data.get("answers")

    if not answers or len(answers) != 5:
        return jsonify({
            "error": "Exactly 5 answers are required."
        }), 400

    # Combine all answers into one paragraph
    combined_text = " ".join(answer.strip() for answer in answers)

    # DistilBERT prediction
    prediction_result = predict(combined_text)

    # Gemini analysis
    insights = generate_insights(
        answers=answers,
        prediction=prediction_result["prediction"],
        confidence=prediction_result["confidence"],
        probabilities=prediction_result["probabilities"]
    )

    return jsonify({
        "prediction": prediction_result["prediction"],
        "confidence": prediction_result["confidence"],
        "probabilities": prediction_result["probabilities"],
        "analysis": insights
    })


if __name__ == "__main__":
    app.run(debug=True)