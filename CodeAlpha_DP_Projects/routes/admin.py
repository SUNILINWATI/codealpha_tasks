from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import flash

from database.db import mysql

admin_bp = Blueprint(
    "admin_bp",
    __name__
)


# ------------------------
# Admin Login
# ------------------------

@admin_bp.route("/admin")
def admin_login():

    return render_template("admin/login.html")


# ------------------------
# Dashboard
# ------------------------

@admin_bp.route("/admin/dashboard")
def admin_dashboard():

    cur = mysql.connection.cursor()

    # Total Users
    cur.execute("SELECT COUNT(*) total FROM users")
    users = cur.fetchone()["total"]

    # Total Predictions
    cur.execute("SELECT COUNT(*) total FROM predictions")
    predictions = cur.fetchone()["total"]

    # Heart
    cur.execute("""

        SELECT COUNT(*) total

        FROM predictions

        WHERE disease='Heart Disease'

    """)

    heart = cur.fetchone()["total"]

    # Diabetes
    cur.execute("""

        SELECT COUNT(*) total

        FROM predictions

        WHERE disease='Diabetes'

    """)

    diabetes = cur.fetchone()["total"]

    # Breast Cancer
    cur.execute("""

        SELECT COUNT(*) total

        FROM predictions

        WHERE disease='Breast Cancer'

    """)

    breast = cur.fetchone()["total"]

    # Latest Predictions
    cur.execute("""

        SELECT

            patient_name,

            disease,

            probability,

            risk_level,

            created_at

        FROM predictions

        ORDER BY created_at DESC

        LIMIT 10

    """)

    history = cur.fetchall()

    cur.close()

    return render_template(

        "admin/dashboard.html",

        users=users,

        predictions=predictions,

        heart=heart,

        diabetes=diabetes,

        breast=breast,

        history=history

    )


# ------------------------
# Users
# ------------------------

@admin_bp.route("/admin/users")
def admin_users():

    cur = mysql.connection.cursor()

    cur.execute("""

        SELECT *

        FROM users

        ORDER BY id DESC

    """)

    users = cur.fetchall()

    cur.close()

    return render_template(

        "admin/users.html",

        users=users

    )


# ------------------------
# Predictions
# ------------------------

@admin_bp.route("/admin/predictions")
def admin_predictions():

    cur = mysql.connection.cursor()

    cur.execute("""

        SELECT *

        FROM predictions

        ORDER BY created_at DESC

    """)

    predictions = cur.fetchall()

    cur.close()

    return render_template(

        "admin/predictions.html",

        predictions=predictions

    )


# ------------------------
# Delete User
# ------------------------

@admin_bp.route("/admin/delete_user/<int:id>")
def delete_user(id):

    cur = mysql.connection.cursor()

    cur.execute(

        "DELETE FROM users WHERE id=%s",

        (id,)

    )

    mysql.connection.commit()

    cur.close()

    flash(

        "User Deleted Successfully",

        "success"

    )

    return redirect("/admin/users")


# ------------------------
# Delete Prediction
# ------------------------

@admin_bp.route("/admin/delete_prediction/<int:id>")
def delete_prediction(id):

    cur = mysql.connection.cursor()

    cur.execute(

        "DELETE FROM predictions WHERE id=%s",

        (id,)

    )

    mysql.connection.commit()

    cur.close()

    flash(

        "Prediction Deleted Successfully",

        "success"

    )

    return redirect("/admin/predictions")