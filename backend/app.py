from flask import Flask, request, jsonify
from flask_cors import CORS
from predictor import predict_text
from llm import generate_insights
from config import LABELS
from collections import Counter

app = Flask(__name__)
CORS(app)

# session storage (simple in-memory)
answers = []
question_predictions = []

def infer_prediction_from_answers(answers, current_label):
    text = " ".join([item["answer"] for item in answers]).lower()
    if current_label != "Normal":
        return current_label

    suicidal_keywords = ["suicidal", "kill myself", "end my life", "die", "worthless", "no reason to live"]
    depression_keywords = ["depressed", "sad", "hopeless", "low", "empty", "crying", "cry", "tired", "miserable"]
    stress_keywords = ["stress", "stressed", "anxious", "anxiety", "overwhelmed", "pressure", "tense", "worried"]

    if any(word in text for word in suicidal_keywords):
        return "Suicidal"

    if any(word in text for word in depression_keywords):
        return "Depression"

    if any(word in text for word in stress_keywords):
        return "Stress"

    return current_label


@app.route("/")
def home():
    return jsonify({"message": "Mentify Backend Running!"})


# -------------------------
# STEP 1: Each question
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    question = data.get("question")
    answer = data.get("answer")

    if not answer:
        return jsonify({"error": "answer required"}), 400

    prediction_input = f"{question} {answer}"
    prediction, confidence, probs = predict_text(prediction_input)

    # store answer
    answers.append({
        "question": question,
        "answer": answer
    })

    # store prediction
    question_predictions.append({
        "question": question,
        "answer": answer,
        "prediction": prediction,
        "confidence": confidence
    })

    return jsonify({
        "prediction": prediction,
        "confidence": confidence,
        "all_probabilities": probs
    })


# -------------------------
# STEP 2: FINAL RESULT (after 5 Qs)
# -------------------------
@app.route("/final", methods=["POST"])
def final():

    if len(question_predictions) < 5:
        return jsonify({"error": "At least 5 answers are required to generate the final result."}), 400

    # majority vote
    all_preds = [q["prediction"] for q in question_predictions]
    overall_prediction = Counter(all_preds).most_common(1)[0][0]
    adjusted_prediction = infer_prediction_from_answers(answers, overall_prediction)

    # call LLM
    llm_result = generate_insights(
        answers=answers,
        overall_prediction=overall_prediction,
        question_predictions=question_predictions
    )

    display_prediction = adjusted_prediction
    final_label = llm_result.get("final_label")
    if final_label and final_label in LABELS:
        display_prediction = final_label

    # reset session
    answers.clear()
    question_predictions.clear()

    return jsonify({
        "overall_prediction": overall_prediction,
        "display_prediction": display_prediction,
        "insights": llm_result
    })


if __name__ == "__main__":
    app.run(debug=True)