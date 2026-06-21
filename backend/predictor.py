import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from config import MODEL_PATH, LABELS

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()


def predict_text(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probs = torch.softmax(logits, dim=1).cpu().numpy()[0]

    pred_index = int(np.argmax(probs))
    prediction = LABELS[pred_index]
    confidence = float(probs[pred_index])

    prob_dict = {
        LABELS[i]: float(probs[i]) for i in range(len(LABELS))
    }

    return prediction, confidence, prob_dict