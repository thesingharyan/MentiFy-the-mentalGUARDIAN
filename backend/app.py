from flask import Flask, request, jsonify
from flask_cors import CORS

from predictor import predict
from llm import generate_insights

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Mentify AI Backend is Running"
    })


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No input provided"}), 400

        answers = data.get("answers")

        # -----------------------------
        # VALIDATION
        # -----------------------------
        if not answers:
            return jsonify({"error": "Answers field is required"}), 400

        if len(answers) != 5:
            return jsonify({"error": "Exactly 5 answers required"}), 400

        # Ensure all inputs are strings
        cleaned_answers = [str(a).strip() for a in answers if a]

        if len(cleaned_answers) != 5:
            return jsonify({"error": "All 5 answers must be non-empty"}), 400

        # -----------------------------
        # STEP 1: ML PREDICTION
        # -----------------------------
        combined_text = " ".join(cleaned_answers)
        prediction_result = predict(combined_text)

        # -----------------------------
        # STEP 2: LLM INSIGHTS
        # -----------------------------
        insights = generate_insights(
            answers=cleaned_answers,
            prediction=prediction_result["prediction"],
            confidence=prediction_result["confidence"],
            probabilities=prediction_result["probabilities"]
        )

        # -----------------------------
        # FINAL RESPONSE
        # -----------------------------
        return jsonify({
            "success": True,
            "input": cleaned_answers,
            "prediction": prediction_result["prediction"],
            "confidence": prediction_result["confidence"],
            "probabilities": prediction_result["probabilities"],
            "analysis": insights
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500



if __name__ == "__main__":
    app.run(debug=True)