from llm import generate_insights

answers = [
    "I feel stressed all day.",
    "I can't sleep properly.",
    "I overthink everything.",
    "I feel exhausted.",
    "I cannot focus."
]

prediction = "Stress"

confidence = 0.98

probabilities = {
    "Stress":0.98,
    "Anxiety":0.01,
    "Depression":0.01
}

result = generate_insights(
    answers,
    prediction,
    confidence,
    probabilities
)

print(result)