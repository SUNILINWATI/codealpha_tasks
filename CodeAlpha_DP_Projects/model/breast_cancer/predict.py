import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL = os.path.join(
    BASE_DIR,
    "saved_models",
    "breast_model.pkl"
)

SCALER = os.path.join(
    BASE_DIR,
    "saved_models",
    "breast_scaler.pkl"
)

FEATURES = os.path.join(
    BASE_DIR,
    "saved_models",
    "breast_features.pkl"
)

ENCODER = os.path.join(
    BASE_DIR,
    "saved_models",
    "breast_encoder.pkl"
)

# Load Model
model = joblib.load(MODEL)
scaler = joblib.load(SCALER)
feature_names = joblib.load(FEATURES)
encoder = joblib.load(ENCODER)


def predict_breast(form_data):

    sample = {}

    for feature in feature_names:

        sample[feature] = float(form_data[feature])
    

    sample = pd.DataFrame([sample])

    sample = scaler.transform(sample)

    prediction = model.predict(sample)[0]

    probability = model.predict_proba(sample)[0]

    prediction_text = encoder.inverse_transform([prediction])[0]

    # Probabilities
    benign_index = list(encoder.classes_).index("B")
    malignant_index = list(encoder.classes_).index("M")

    benign_probability = round(probability[benign_index] * 100, 2)
    malignant_probability = round(probability[malignant_index] * 100, 2)

# ---------------- Prediction ---------------- #

    if prediction_text == "M":

        status = "Malignant (Cancer Detected)"
        confidence = malignant_probability

        if confidence >= 80:
            risk = "HIGH"

        elif confidence >= 60:
            risk = "MEDIUM"

        else:
            risk = "LOW"

    else:

        status = "Benign (No Cancer)"
        confidence = benign_probability
        risk = "LOW"

    return {

        "prediction": int(prediction),

        "prediction_text": prediction_text,

        "status": status,

        "probability": confidence,

        "risk": risk

    }