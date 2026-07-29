from flask import Blueprint
from flask import render_template
from flask import request

from database.db import mysql
from model.predict import predict_disease

prediction_bp = Blueprint(
    "prediction_bp",
    __name__
)


@prediction_bp.route("/heart-prediction")
def heart_prediction():

    return render_template("prediction.html")


@prediction_bp.route("/predict", methods=["POST"])
def predict():

    form_data = request.form.to_dict()

    patient_name = form_data.get("patient_name", "Unknown")

    result = predict_disease(form_data)

    cur = mysql.connection.cursor()

    cur.execute("""

        INSERT INTO predictions(

            patient_name,

            disease,

            prediction,

            probability,

            risk_level

        )

        VALUES(%s,%s,%s,%s,%s)

    """,(

        patient_name,

        "Heart Disease",

        result["prediction"],

        result["probability"],

        result["risk"]

    ))

    mysql.connection.commit()

    cur.close()

    return render_template(

        "result.html",

        result=result

    )