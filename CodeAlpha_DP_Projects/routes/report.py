from flask import Blueprint
from flask import send_file
from flask import session

from database.db import mysql
from routes.auth_guard import login_required
from utils.pdf_generator import generate_pdf

report_bp = Blueprint(
    "report_bp",
    __name__
)


@report_bp.route("/download_report/<int:prediction_id>")
@login_required
def download_report(prediction_id):

    cur = mysql.connection.cursor()

    cur.execute("""

        SELECT

            patient_name,

            disease,

            prediction,

            probability,

            risk_level

        FROM predictions

        WHERE id=%s

        AND user_id=%s

    """,(

        prediction_id,

        session["user_id"]

    ))

    row = cur.fetchone()

    cur.close()

    if not row:

        return "Report Not Found",404

    recommendation = ""

    if row["risk_level"] == "HIGH":

        recommendation = """
        Consult a specialist immediately.
        Maintain healthy diet.
        Follow prescribed medication.
        Schedule regular checkups.
        """

    elif row["risk_level"] == "MEDIUM":

        recommendation = """
        Exercise regularly.
        Maintain healthy BMI.
        Reduce sugar and cholesterol.
        """

    else:

        recommendation = """
        Continue healthy lifestyle.
        Annual health checkup recommended.
        """

    pdf = generate_pdf(
        patient_name=row["patient_name"],
        disease=row["disease"],
        prediction="Positive" if row["prediction"] == 1 else "Negative",
        probability=row["probability"],
        risk=row["risk_level"],
        recommendation=recommendation
    )

    import os

    print("Generated PDF:", pdf)
    print("Exists:", os.path.exists(pdf))

    if not os.path.exists(pdf):
        return "PDF file was not created.", 500

    return send_file(
        os.path.abspath(pdf),
        as_attachment=True,
        download_name=os.path.basename(pdf),
        mimetype="application/pdf"
    )