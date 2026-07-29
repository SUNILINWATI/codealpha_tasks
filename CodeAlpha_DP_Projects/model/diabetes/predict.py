import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL = os.path.join(BASE_DIR, "saved_models", "diabetes_model.pkl")
FEATURES = os.path.join(BASE_DIR, "saved_models", "diabetes_features.pkl")
SCALER = os.path.join(BASE_DIR, "saved_models", "diabetes_scaler.pkl")
USE_SCALER = os.path.join(BASE_DIR, "saved_models", "use_scaler.pkl")

model = joblib.load(MODEL)
feature_names = joblib.load(FEATURES)
scaler = joblib.load(SCALER)
use_scaler = joblib.load(USE_SCALER)


def predict_diabetes(form_data):

    sample = {}

    # Read form data
    for feature in feature_names:
        sample[feature] = float(form_data[feature])

    sample_df = pd.DataFrame([sample])

    # Scale only if Logistic Regression is selected
    if use_scaler:
        sample_input = scaler.transform(sample_df)
    else:
        sample_input = sample_df

    # Prediction
    prediction = model.predict(sample_input)[0]
    probability = model.predict_proba(sample_input)[0]

    healthy_prob = round(probability[0] * 100, 2)
    diabetes_prob = round(probability[1] * 100, 2)

    if prediction == 1:
        status = "Diabetes Detected"
        confidence = diabetes_prob
    else:
        status = "Healthy"
        confidence = healthy_prob

    # =========================
    # SMART RISK CALCULATION
    # =========================

    glucose = float(form_data["Glucose"])
    bmi = float(form_data["BMI"])
    insulin = float(form_data["Insulin"])
    age = float(form_data["Age"])
    pregnancies = float(form_data["Pregnancies"])
    blood_pressure = float(form_data["BloodPressure"])

    if prediction == 0:

        risk = "LOW"

    else:

        # HIGH Risk
        if (
            confidence >= 80 or
            glucose >= 200 or
            bmi >= 40 or
            insulin >= 300 or
            age >= 60 or
            pregnancies >= 8 or
            blood_pressure >= 95
        ):
            risk = "HIGH"

        # MEDIUM Risk
        elif (
            confidence >= 55 or
            glucose >= 160 or
            bmi >= 35 or
            insulin >= 180 or
            age >= 45
        ):
            risk = "MEDIUM"

        # LOW Risk
        else:
            risk = "LOW"

    return {

        "prediction": int(prediction),

        "status": status,

        "probability": confidence,

        "risk": risk

    }