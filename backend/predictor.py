import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from config import HF_MODEL, LABELS

# Load tokenizer and model once (important for performance)
tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)
model = AutoModelForSequenceClassification.from_pretrained(HF_MODEL)

# Set device (GPU if available, else CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()


def predict(text: str):
    """
    Takes user text input and returns:
    - predicted label
    - confidence score
    - probability distribution
    """

    # Tokenize input
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    # Move tensors to device
    inputs = {key: val.to(device) for key, val in inputs.items()}

    # Disable gradient calculation for inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Convert logits to probabilities
    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=1).cpu().numpy()[0]

    # Get prediction index
    pred_index = int(np.argmax(probs))

    # Map to label
    prediction = LABELS[pred_index]

    confidence = float(probs[pred_index])

    # Build probability dictionary
    probabilities = {
        LABELS[i]: float(probs[i])
        for i in range(len(LABELS))
    }

    print("Loaded model from:", HF_MODEL)
    print(model.config._name_or_path)
    
    return {
        "prediction": prediction,
        "confidence": round(confidence, 4),
        "probabilities": probabilities
    }