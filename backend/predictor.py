import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from config import HF_MODEL, MAX_LENGTH

# Load tokenizer and model (loads once when Flask starts)
tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)
model = AutoModelForSequenceClassification.from_pretrained(HF_MODEL)

# Set model to evaluation mode
model.eval()


def predict(text):
    """
    Predict mental health category from input text.

    Returns:
        {
            "prediction": "...",
            "confidence": 0.95,
            "probabilities": {
                ...
            }
        }
    """

    # Tokenize input
    inputs = tokenizer(
        text,
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH,
        return_tensors="pt"
    )

    # Disable gradient calculations
    with torch.no_grad():
        outputs = model(**inputs)

    # Convert logits to probabilities
    probabilities = torch.softmax(outputs.logits, dim=1)[0]

    # Predicted class index
    predicted_index = torch.argmax(probabilities).item()

    # Label name
    predicted_label = model.config.id2label[str(predicted_index)] \
        if isinstance(model.config.id2label, dict) and str(predicted_index) in model.config.id2label \
        else model.config.id2label[predicted_index]

    # Confidence
    confidence = probabilities[predicted_index].item()

    # Probability dictionary
    probability_dict = {}

    for i, prob in enumerate(probabilities):
        label = model.config.id2label[str(i)] \
            if isinstance(model.config.id2label, dict) and str(i) in model.config.id2label \
            else model.config.id2label[i]

        probability_dict[label] = round(prob.item(), 4)

    return {
    "input_text": text,
    "prediction": predicted_label,
    "confidence": round(confidence, 4),
    "probabilities": probability_dict
}