from datetime import datetime

from flask import Blueprint
from flask import render_template
from flask import request
from flask import session

from database.db import mysql
from model.heart_disease.predict import predict_heart
from routes.auth_guard import login_required

heart_bp = Blueprint(
    "heart_bp",
    __name__
)


@heart_bp.route("/heart")
@login_required
def heart():

    return render_template("heart_disease.html")


@heart_bp.route("/heart_predict", methods=["POST"])
@login_required
def heart_predict():

    form = request.form.to_dict()

    patient_name = form.get("patient_name")
    patient_age = form.get("patient_age")

    result = predict_heart(form)

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO predictions
        (
            user_id,
            patient_name,
            patient_age,
            disease,
            prediction,
            probability,
            risk_level
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s)
    """, (

        session["user_id"],
        patient_name,
        patient_age,
        "Heart Disease",
        result["prediction"],
        result["probability"],
        result["risk"]

    ))

    mysql.connection.commit()

    prediction_id = cur.lastrowid

    cur.close()

    return render_template(

        "result_heart_disease.html",

        result=result,

        patient_name=patient_name,

        patient_age=patient_age,

        prediction_id=prediction_id,

        date=datetime.now().strftime("%d-%m-%Y %I:%M %p")

    )