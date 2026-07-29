from flask import Blueprint
from flask import render_template, session
from flask import request
from datetime import datetime

from database.db import mysql
from model.diabetes.predict import predict_diabetes
from routes.auth_guard import login_required

diabetes_bp = Blueprint(
    "diabetes_bp",
    __name__
)


@diabetes_bp.route("/diabetes")
@login_required
def diabetes():

    return render_template("diabetes.html")


@diabetes_bp.route("/diabetes_predict", methods=["POST"])
@login_required
def diabetes_predict():

    form = request.form.to_dict()

    patient_name = form["patient_name"]
    patient_age = form["patient_age"]

    # Model ke liye Age feature create karo
    form["Age"] = patient_age

    result = predict_diabetes(form)

    cur = mysql.connection.cursor()

    cur.execute("""

        INSERT INTO predictions(

            user_id,

            patient_name,

            patient_age,

            disease,

            prediction,

            probability,

            risk_level

        )

        VALUES(%s,%s,%s,%s,%s,%s,%s)

    """,(

        session["user_id"],

        patient_name,

        patient_age,

        "Diabetes",

        result["prediction"],

        result["probability"],

        result["risk"]

    ))

    mysql.connection.commit()

    prediction_id = cur.lastrowid

    cur.close()

    return render_template(

        "result_diabetes.html",

        result=result,

        patient_name=patient_name,
        patient_age=patient_age,

        prediction_id=prediction_id,

        date=datetime.now().strftime("%d-%m-%Y %I:%M %p")

    )