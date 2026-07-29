from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    request,
    send_file
)

from utils.pdf_generator import generate_pdf
from database.db import cursor, conn

history_bp = Blueprint(
    "history",
    __name__
)


# ==========================================================
# PREDICTION HISTORY
# ==========================================================

@history_bp.route("/history")
def history():

    # -----------------------------
    # LOGIN CHECK
    # -----------------------------

    if "user_id" not in session:

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    user_id = session["user_id"]

    # -----------------------------
    # SEARCH
    # -----------------------------

    search = request.args.get(
        "search",
        ""
    ).strip()

    # -----------------------------
    # STATUS FILTER
    # -----------------------------

    status = request.args.get(
        "status",
        "All"
    )

    # -----------------------------
    # SQL QUERY
    # -----------------------------

    sql = """

    SELECT

        id,

        fullname,

        age,

        annual_income,

        loan_amount,

        credit_score,

        status,

        risk,

        confidence,

        recommendation,

        created_at

    FROM predictions

    WHERE user_id=%s

    """

    params = [user_id]

    # -----------------------------
    # SEARCH FILTER
    # -----------------------------

    if search:

        sql += """

        AND fullname LIKE %s

        """

        params.append(f"%{search}%")

    # -----------------------------
    # STATUS FILTER
    # -----------------------------

    if status != "All":

        sql += """

        AND status=%s

        """

        params.append(status)

    # -----------------------------
    # SORT
    # -----------------------------

    sql += """

    ORDER BY created_at DESC

    """

    cursor.execute(
        sql,
        tuple(params)
    )

    history = cursor.fetchall()

    # -----------------------------
    # DEBUG
    # -----------------------------

    print("=" * 70)

    print("History Records :", len(history))

    print("=" * 70)
    return render_template(
        "history.html",
        history=history,
        search=search,
        status=status,
        fullname=session.get("name")
    )
# ==========================================================
# VIEW PREDICTION
# ==========================================================

@history_bp.route("/view_prediction/<int:prediction_id>")
def view_prediction(prediction_id):

    if "user_id" not in session:

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    cursor.execute("""

        SELECT

            id,
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
            recommendation,
            created_at

        FROM predictions

        WHERE id=%s

        AND user_id=%s

    """,
    (
        prediction_id,
        session["user_id"]
    ))

    prediction = cursor.fetchone()

    if prediction is None:

        flash(
            "Prediction not found.",
            "danger"
        )

        return redirect(
            url_for("history.history")
        )

    return render_template(

        "view_prediction.html",

        prediction=prediction,

        prediction_id=prediction_id

    )


# ==========================================================
# DELETE PREDICTION
# ==========================================================

@history_bp.route("/delete_prediction/<int:prediction_id>")
def delete_prediction(prediction_id):

    if "user_id" not in session:

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    cursor.execute("""

        SELECT id

        FROM predictions

        WHERE id=%s

        AND user_id=%s

    """,
    (
        prediction_id,
        session["user_id"]
    ))

    check = cursor.fetchone()

    if check is None:

        flash(
            "Prediction not found.",
            "danger"
        )

        return redirect(
            url_for("history.history")
        )

    cursor.execute("""

        DELETE FROM predictions

        WHERE id=%s

        AND user_id=%s

    """,
    (
        prediction_id,
        session["user_id"]
    ))

    conn.commit()

    flash(
        "Prediction deleted successfully.",
        "success"
    )

    return redirect(
        url_for("history.history")
  )
# ==========================================================
# DOWNLOAD PDF
# ==========================================================

@history_bp.route("/download_prediction/<int:prediction_id>")
def download_prediction(prediction_id):

    if "user_id" not in session:

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    cursor.execute("""

        SELECT

            id,
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
            recommendation,
            created_at

        FROM predictions

        WHERE id=%s

        AND user_id=%s

    """,
    (
        prediction_id,
        session["user_id"]
    ))

    prediction = cursor.fetchone()

    if prediction is None:

        flash(
            "Prediction not found.",
            "danger"
        )

        return redirect(
            url_for("history.history")
        )

    pdf_path = generate_pdf(prediction)

    return send_file(

        pdf_path,

        as_attachment=True,

        download_name=f"Loan_Report_{prediction_id}.pdf"

    )

