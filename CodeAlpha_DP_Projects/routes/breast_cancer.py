from flask import Blueprint, render_template, request, session
from datetime import datetime

from database.db import mysql
from model.breast_cancer.predict import predict_breast
from routes.auth_guard import login_required

breast_bp = Blueprint(
    "breast_bp",
    __name__
)


# ---------------- Breast Cancer Page ---------------- #

@breast_bp.route("/breast", methods=["GET"])
@login_required
def breast():
    return render_template("breast_cancer.html")


# ---------------- Prediction ---------------- #

@breast_bp.route("/breast_predict", methods=["POST"])
@login_required
def breast_predict():

    form = request.form.to_dict()

    patient_name = form.get("patient_name", "")

    result = predict_breast(form)

    cur = mysql.connection.cursor()
    print("SESSION =", dict(session))
    print("USER ID =", session.get("user_id"))

    cur.execute(
        "SELECT id, name FROM users WHERE id=%s",
        (session.get("user_id"),)
    )

    print("DB USER =", cur.fetchone())

    cur.execute("""
        INSERT INTO predictions
        (
            user_id,
            patient_name,
            disease,
            prediction,
            probability,
            risk_level
        )
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        session["user_id"],
        patient_name,
        "Breast Cancer",
        result["prediction"],
        result["probability"],
        result["risk"]
    ))

    mysql.connection.commit()

    prediction_id = cur.lastrowid

    cur.close()

    return render_template(
        "result_breast_cancer.html",
        result=result,
        patient_name=patient_name,
        prediction_id=prediction_id,
        date=datetime.now().strftime("%d-%m-%Y %I:%M %p")
    )