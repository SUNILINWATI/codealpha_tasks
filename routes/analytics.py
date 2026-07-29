from flask import Blueprint, render_template, session, redirect, url_for, flash
from database.db import cursor

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics")
def analytics():

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth.login"))

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM predictions
        GROUP BY status
    """)
    status_data = cursor.fetchall()

    cursor.execute("""
        SELECT risk, COUNT(*)
        FROM predictions
        GROUP BY risk
    """)
    risk_data = cursor.fetchall()

    status_labels = [row[0] for row in status_data]
    status_values = [row[1] for row in status_data]

    risk_labels = [row[0] for row in risk_data]
    risk_values = [row[1] for row in risk_data]

    return render_template(
        "analytics.html",
        status_labels=status_labels,
        status_values=status_values,
        risk_labels=risk_labels,
        risk_values=risk_values
    )