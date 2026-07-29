import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL = os.path.join(BASE_DIR, "saved_models", "heart_model.pkl")
SCALER = os.path.join(BASE_DIR, "saved_models", "heart_scaler.pkl")
FEATURES = os.path.join(BASE_DIR, "saved_models", "heart_features.pkl")

model = joblib.load(MODEL)
scaler = joblib.load(SCALER)
feature_names = joblib.load(FEATURES)


def predict_heart(form_data):

    field_map = {

        "age": "patient_age",
        "sex": "sex",
        "resting_bp_systolic": "systolic_bp",
        "resting_bp_diastolic": "diastolic_bp",
        "cholesterol_total": "cholesterol_total",
        "fasting_blood_sugar": "fasting_blood_sugar",
        "bmi": "bmi",
        "resting_heart_rate": "resting_heart_rate",
        "chest_pain_type": "chest_pain_type",
        "exercise_induced_angina": "exercise_induced_angina",
        "st_depression": "st_depression",
        "family_history": "family_history",
        "smoker_status": "smoker_status"

    }

    sample = {}

    for feature in feature_names:

        html_name = field_map[feature]

        value = form_data.get(html_name)

        if value is None or value == "":
            raise ValueError(f"Missing field : {html_name}")

        sample[feature] = value

    sample = pd.DataFrame([sample])

    # Encode

    sample["sex"] = sample["sex"].replace({
        "Male": 1,
        "Female": 0
    })

    sample["chest_pain_type"] = sample["chest_pain_type"].replace({
        "Typical Angina": 0,
        "Atypical Angina": 1,
        "Non-anginal Pain": 2,
        "Asymptomatic": 3
    })

    sample["exercise_induced_angina"] = sample["exercise_induced_angina"].replace({
        "No": 0,
        "Yes": 1
    })

    sample["family_history"] = sample["family_history"].replace({
        "No": 0,
        "Yes": 1
    })

    sample["smoker_status"] = sample["smoker_status"].replace({
        "Never": 0,
        "Former": 1,
        "Current": 2
    })

    sample = sample.astype(float)

    sample = scaler.transform(sample)

    prediction = model.predict(sample)[0]

    probability = model.predict_proba(sample)[0]

    healthy = round(probability[0] * 100, 2)
    disease = round(probability[1] * 100, 2)

    if prediction == 1:
        status = "Heart Disease Detected"
        confidence = disease
    else:
        status = "Healthy"
        confidence = healthy

    age = float(form_data["patient_age"])
    sys = float(form_data["systolic_bp"])
    dia = float(form_data["diastolic_bp"])
    chol = float(form_data["cholesterol_total"])
    sugar = float(form_data["fasting_blood_sugar"])
    bmi = float(form_data["bmi"])

    if prediction == 0:

        risk = "LOW"

    else:

        if (
            confidence >= 80
            or age >= 65
            or sys >= 180
            or dia >= 110
            or chol >= 300
            or sugar >= 180
            or bmi >= 35
        ):
            risk = "HIGH"

        elif (
            confidence >= 55
            or age >= 50
            or sys >= 140
            or dia >= 90
            or chol >= 240
            or sugar >= 140
            or bmi >= 30
        ):
            risk = "MEDIUM"

        else:
            risk = "LOW"

    return {

        "prediction": int(prediction),
        "status": status,
        "probability": confidence,
        "risk": risk

    }