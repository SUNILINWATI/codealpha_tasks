from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash
)

from database.db import cursor

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/dashboard")
def dashboard():

    # =====================================================
    # LOGIN CHECK
    # =====================================================

    if "user_id" not in session:

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    user_id = session["user_id"]

    # =====================================================
    # TOTAL USERS
    # =====================================================

    cursor.execute("""

        SELECT COUNT(*)

        FROM users

    """)

    total_users = cursor.fetchone()[0]

    # =====================================================
    # TOTAL PREDICTIONS
    # =====================================================

    cursor.execute("""

        SELECT COUNT(*)

        FROM predictions

        WHERE user_id=%s

    """, (user_id,))

    total_predictions = cursor.fetchone()[0]

    # =====================================================
    # APPROVED LOANS
    # =====================================================

    cursor.execute("""

        SELECT COUNT(*)

        FROM predictions

        WHERE user_id=%s

        AND status='Approved'

    """, (user_id,))

    approved = cursor.fetchone()[0]

    # =====================================================
    # REJECTED LOANS
    # =====================================================

    cursor.execute("""

        SELECT COUNT(*)

        FROM predictions

        WHERE user_id=%s

        AND status='Rejected'

    """, (user_id,))

    rejected = cursor.fetchone()[0]

    # =====================================================
    # AVERAGE AI CREDIT SCORE
    # =====================================================

    cursor.execute("""

        SELECT AVG(credit_score)

        FROM predictions

        WHERE user_id=%s

    """, (user_id,))

    avg_score = cursor.fetchone()[0]

    if avg_score is None:

        average_credit_score = 0

    else:

        average_credit_score = round(avg_score)

    # =====================================================
    # APPROVAL RATE
    # =====================================================

    if total_predictions > 0:

        approval_rate = round(

            (approved / total_predictions) * 100,

            2

        )

        rejection_rate = round(

            (rejected / total_predictions) * 100,

            2

        )

    else:

        approval_rate = 0

        rejection_rate = 0

    print("=" * 70)
    print("DASHBOARD")
    print("=" * 70)
    print("User ID :", user_id)
    print("Total Predictions :", total_predictions)
    print("Approved :", approved)
    print("Rejected :", rejected)
    print("Average Score :", average_credit_score)
    print("=" * 70)
    
        # =====================================================
    # RECENT PREDICTIONS
    # =====================================================

    cursor.execute("""

        SELECT
            fullname,
            credit_score,
            risk,
            status,
            created_at

        FROM predictions

        WHERE user_id=%s

        ORDER BY created_at DESC

        LIMIT 5

    """, (user_id,))

    recent_predictions = cursor.fetchall()

    # =====================================================
    # RISK COUNT
    # =====================================================

    cursor.execute("""

        SELECT COUNT(*)

        FROM predictions

        WHERE user_id=%s

        AND risk='Low Risk'

    """, (user_id,))

    low_risk = cursor.fetchone()[0]

    cursor.execute("""

        SELECT COUNT(*)

        FROM predictions

        WHERE user_id=%s

        AND risk='Medium Risk'

    """, (user_id,))

    medium_risk = cursor.fetchone()[0]

    cursor.execute("""

        SELECT COUNT(*)

        FROM predictions

        WHERE user_id=%s

        AND risk='High Risk'

    """, (user_id,))

    high_risk = cursor.fetchone()[0]

    # =====================================================
    # MONTHLY PREDICTIONS
    # =====================================================

    cursor.execute("""

        SELECT
            MONTH(created_at),
            COUNT(*)

        FROM predictions

        WHERE user_id=%s

        GROUP BY MONTH(created_at)

        ORDER BY MONTH(created_at)

    """, (user_id,))

    monthly_data = cursor.fetchall()

    months = []

    monthly_predictions = []

    for row in monthly_data:

        months.append(row[0])

        monthly_predictions.append(row[1])

    # =====================================================
    # PIE CHART DATA
    # =====================================================

    risk_chart = {

        "Low": low_risk,

        "Medium": medium_risk,

        "High": high_risk

    }

    approval_chart = {

        "Approved": approved,

        "Rejected": rejected

    }

    # =====================================================
    # DASHBOARD DEBUG
    # =====================================================

    print("\nRecent Predictions")

    for row in recent_predictions:

        print(row)

    print("\nRisk Summary")

    print("Low Risk :", low_risk)

    print("Medium Risk :", medium_risk)

    print("High Risk :", high_risk)

    print("=" * 70)
    
        # =====================================================
    # RENDER DASHBOARD
    # =====================================================

    return render_template(

        "dashboard.html",

        # Logged User
        fullname=session.get("name"),

        # Dashboard Cards
        total_users=total_users,

        total_predictions=total_predictions,

        approved=approved,

        rejected=rejected,

        average_credit_score=average_credit_score,

        approval_rate=approval_rate,

        rejection_rate=rejection_rate,

        # Risk Statistics
        low_risk=low_risk,

        medium_risk=medium_risk,

        high_risk=high_risk,

        # Charts
        months=months,

        monthly_predictions=monthly_predictions,

        risk_chart=risk_chart,

        approval_chart=approval_chart,

        # Table
        recent_predictions=recent_predictions

    )