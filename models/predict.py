import joblib
import pandas as pd

# ==========================
# Load Saved Objects
# ==========================

model = joblib.load("models/best_model.pkl")
scaler = joblib.load("models/scaler.pkl")
encoders = joblib.load("models/encoders.pkl")
feature_names = joblib.load("models/feature_names.pkl")


def predict_credit(user_data):
    """
    user_data should be a dictionary.
    """

    # Convert dictionary to DataFrame
    df = pd.DataFrame([user_data])

    # ==========================
    # Apply Label Encoding
    # ==========================

    for column, encoder in encoders.items():

        if column in df.columns:

            value = str(df[column].iloc[0])

            if value not in encoder.classes_:
                value = encoder.classes_[0]

            df[column] = encoder.transform([value])

    # ==========================
    # Arrange Columns
    # ==========================

    df = df[feature_names]

    # ==========================
    # Scale Data
    # ==========================

    df_scaled = scaler.transform(df)

    # ==========================
    # Prediction
    # ==========================

    prediction = model.predict(df_scaled)[0]
    probability = model.predict_proba(df_scaled)[0]

    confidence = round(max(probability) * 100, 2)

    # ==========================
    # Credit Score
    # ==========================

    credit_score = int(300 + confidence * 5.5)

    if credit_score > 850:
        credit_score = 850

    # ==========================
    # AI Prediction
    # ==========================

    if prediction == 1:
        status = "Approved"
    else:
        status = "Rejected"

    # ==========================
    # Risk Level
    # ==========================

    if credit_score >= 750:
        risk = "Low Risk"

    elif credit_score >= 650:
        risk = "Medium Risk"

    else:
        risk = "High Risk"

    # ==========================
    # Recommendation
    # ==========================

    if status == "Approved":
        recommendation = "Eligible for Loan"
    else:
        recommendation = "Improve Credit History"

    # ==========================
    # Return Result
    # ==========================

    return {

        "prediction": int(prediction),

        "status": status,

        "risk": risk,

        "credit_score": credit_score,

        "confidence": confidence,

        "recommendation": recommendation

    }