from flask import Blueprint
from flask import render_template
from flask import session

from database.db import mysql
from routes.auth_guard import login_required

dashboard_bp = Blueprint(
    "dashboard_bp",
    __name__
)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    cur = mysql.connection.cursor()

    # ---------------- Dashboard Cards ---------------- #

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM predictions
        WHERE user_id=%s
    """, (session["user_id"],))
    total = cur.fetchone()["total"]

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM predictions
        WHERE user_id=%s
        AND disease='Heart Disease'
    """, (session["user_id"],))
    heart = cur.fetchone()["total"]

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM predictions
        WHERE user_id=%s
        AND disease='Diabetes'
    """, (session["user_id"],))
    diabetes = cur.fetchone()["total"]

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM predictions
        WHERE user_id=%s
        AND disease='Breast Cancer'
    """, (session["user_id"],))
    breast = cur.fetchone()["total"]

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM predictions
        WHERE user_id=%s
        AND risk_level='HIGH'
    """, (session["user_id"],))
    high = cur.fetchone()["total"]


    # ---------------- Disease Distribution ---------------- #

    cur.execute("""
        SELECT disease,
               COUNT(*) AS total
        FROM predictions
        WHERE user_id=%s
        GROUP BY disease
    """, (session["user_id"],))

    disease = cur.fetchall()

    disease_labels = [row["disease"] for row in disease]
    disease_values = [row["total"] for row in disease]


    # ---------------- Risk Distribution ---------------- #

    cur.execute("""
        SELECT risk_level,
               COUNT(*) AS total
        FROM predictions
        WHERE user_id=%s
        GROUP BY risk_level
    """, (session["user_id"],))

    risks = cur.fetchall()

    risk_labels = [row["risk_level"] for row in risks]
    risk_values = [row["total"] for row in risks]


# ---------------- Last 7 Days Predictions ---------------- #

    day_labels = []
    day_values = []

    cur.execute("""
        SELECT
            DATE(created_at) AS day,
            COUNT(*) AS total
        FROM predictions
        WHERE user_id=%s
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at) DESC
        LIMIT 7
    """, (session["user_id"],))

    days = cur.fetchall()

    for row in days:

        day_labels.append(row["day"].strftime("%d %b"))

        day_values.append(row["total"])

    # ---------------- Recent Predictions ---------------- #

    cur.execute("""
        SELECT
            patient_name,
            patient_age,
            disease,
            prediction,
            probability,
            risk_level,
            created_at
        FROM predictions
        WHERE user_id=%s
        ORDER BY created_at DESC
        LIMIT 5            
    """, (session["user_id"],))

    history = cur.fetchall()

    cur.close()
    
    print(day_labels)
    print(day_values)

    return render_template(

        "dashboard.html",

        username=session["user_name"],

        total=total,

        heart=heart,

        diabetes=diabetes,

        breast=breast,

        high=high,

        history=history,

        disease_labels=disease_labels,
        disease_values=disease_values,

        risk_labels=risk_labels,
        risk_values=risk_values,

        day_labels=day_labels,
        day_values=day_values
    )