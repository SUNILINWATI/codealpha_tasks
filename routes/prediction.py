from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    redirect,
    url_for
)

from database.db import conn, cursor

import joblib
import pandas as pd
import numpy as np

prediction_bp = Blueprint(
    "prediction",
    __name__
)

# ==========================================================
# LOAD MODEL
# ==========================================================

model = joblib.load("models/best_model.pkl")
scaler = joblib.load("models/scaler.pkl")
encoders = joblib.load("models/encoders.pkl")
feature_names = joblib.load("models/feature_names.pkl")

print("=" * 70)
print("Credit AI Model Loaded Successfully")
print("Model :", type(model).__name__)
print("=" * 70)


# ==========================================================
# LOAN PREDICTION
# ==========================================================

@prediction_bp.route(
    "/prediction",
    methods=["GET", "POST"]
)
def prediction():

    if "user_id" not in session:

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    result = None

    # =====================================================
    # GET REQUEST
    # =====================================================

    if request.method == "GET":

        return render_template(
            "prediction.html",
            result=result
        )

    # =====================================================
    # POST REQUEST
    # =====================================================

    try:

        print("\n" + "=" * 70)
        print("NEW LOAN PREDICTION")
        print("=" * 70)

        full_name = request.form.get("full_name")

        print("Applicant :", full_name)

        # =====================================================
        # GET FORM DATA
        # =====================================================

        data = {

            "person_age": int(request.form["person_age"]),

            "person_gender": request.form["person_gender"],

            "person_education": request.form["person_education"],

            "person_income": float(request.form["person_income"]),

            "person_emp_exp": int(request.form["person_emp_exp"]),

            "person_home_ownership": request.form["person_home_ownership"],

            "loan_amnt": float(request.form["loan_amnt"]),

            "loan_intent": request.form["loan_intent"],

            "loan_int_rate": float(request.form["loan_int_rate"]),

            "loan_percent_income": float(
                request.form["loan_percent_income"]
            ),

            "cb_person_cred_hist_length": int(
                request.form["cb_person_cred_hist_length"]
            ),

            "credit_score": int(
                request.form["credit_score"]
            ),

            "previous_loan_defaults_on_file":
                request.form[
                    "previous_loan_defaults_on_file"
                ]
        }

        # =====================================================
        # VALIDATION
        # =====================================================

        if data["person_age"] < 18:

            flash(
                "Age must be at least 18 years.",
                "danger"
            )

            return redirect(
                url_for("prediction.prediction")
            )

        if data["person_income"] <= 0:

            flash(
                "Income must be greater than zero.",
                "danger"
            )

            return redirect(
                url_for("prediction.prediction")
            )

        if data["loan_amnt"] <= 0:

            flash(
                "Loan amount must be greater than zero.",
                "danger"
            )

            return redirect(
                url_for("prediction.prediction")
            )

        if data["credit_score"] < 300 or data["credit_score"] > 850:

            flash(
                "Credit Score must be between 300 and 850.",
                "danger"
            )

            return redirect(
                url_for("prediction.prediction")
            )

        # =====================================================
        # CREATE DATAFRAME
        # =====================================================

        df = pd.DataFrame([data])

        print("\nOriginal Input")
        print(df)
        
        # =====================================================
        # ENCODE CATEGORICAL FEATURES
        # =====================================================

        for column, encoder in encoders.items():

            if column in df.columns:

                value = str(df[column].iloc[0]).strip()

                if value not in encoder.classes_:

                    print(f"Unknown value for {column}: {value}")

                    value = encoder.classes_[0]

                df[column] = encoder.transform([value])

        # =====================================================
        # ARRANGE FEATURES
        # =====================================================

        df = df[feature_names]

        print("\nEncoded Data")
        print(df)

        # =====================================================
        # FEATURE SCALING
        # =====================================================

        if type(model).__name__ == "LogisticRegression":

            df = scaler.transform(df)

            print("\nScaling Applied")

        # =====================================================
        # MODEL PREDICTION
        # =====================================================

        prediction = int(model.predict(df)[0])

        probability = model.predict_proba(df)[0]

        print("\nPrediction :", prediction)

        print("Probability :", probability)

        print("Model Classes :", model.classes_)

        # =====================================================
        # STATUS + CONFIDENCE
        # =====================================================

        if prediction == 0:

            status = "Approved"

            confidence = round(
                probability[1] * 100,
                2
            )

        else:

            status = "Rejected"

            confidence = round(
                probability[0] * 100,
                2
            )

        print("\nStatus :", status)

        print("Confidence :", confidence)

        # =====================================================
        # AI CREDIT SCORE
        # =====================================================
        actual_score = data["credit_score"]

        if status == "Approved":
            ai_credit_score = min(
                850,
                actual_score + int(confidence * 0.5)
            )
        else:
            ai_credit_score = max(
                300,
                actual_score - int((100 - confidence) * 0.8)
            )

        # =====================================================
        # RISK LEVEL
        # =====================================================
        if status == "Rejected":
            risk = "High Risk"

        elif ai_credit_score >= 750:
            risk = "Low Risk"

        elif ai_credit_score >= 650:
            risk = "Medium Risk"

        else:
            risk = "High Risk"
        
        # =====================================================
        # RECOMMENDATION
        # =====================================================

        if status == "Approved":

            if risk == "Low Risk":

                recommendation = (
                    "Loan Approved. Excellent credit profile."
                )

            else:

                recommendation = (
                    "Loan Approved with additional verification."
                )

        else:

            recommendation = (
                "Loan Rejected. Improve your credit score, "
                "reduce debt and increase your income before reapplying."
            )

        # =====================================================
        # SAVE PREDICTION
        # =====================================================

        cursor.execute(
            """
            INSERT INTO predictions
            (
                user_id,
                fullname,
                age,
                gender,
                education,
                annual_income,
                employment_experience,
                home_ownership,
                loan_amount,
                loan_purpose,
                interest_rate,
                loan_percent_income,
                credit_history_length,
                credit_score,
                previous_default,
                prediction,
                status,
                risk,
                confidence,
                recommendation
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            (
                session["user_id"],
                full_name,

                data["person_age"],
                data["person_gender"],
                data["person_education"],
                data["person_income"],
                data["person_emp_exp"],
                data["person_home_ownership"],
                data["loan_amnt"],
                data["loan_intent"],
                data["loan_int_rate"],
                data["loan_percent_income"],
                data["cb_person_cred_hist_length"],

                ai_credit_score,

                data["previous_loan_defaults_on_file"],

                prediction,
                status,
                risk,
                confidence,
                recommendation
            )
        )

        conn.commit()

        print("\nPrediction Saved Successfully")

        # =====================================================
        # RESULT
        # =====================================================

        result = {

            "status": status,

            "confidence": confidence,

            "credit_score": ai_credit_score,

            "risk": risk,

            "recommendation": recommendation

        }

    except Exception as e:

        if conn:

            conn.rollback()

        print("Prediction Error :", e)

        flash(
            f"Prediction Error : {e}",
            "danger"
        )

        return redirect(
            url_for("prediction.prediction")
        )

    return render_template(

        "prediction.html",

        result=result

    )