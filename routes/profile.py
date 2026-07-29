from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    request
)

from database.db import cursor, conn

profile_bp = Blueprint(
    "profile",
    __name__
)


# ============================================
# PROFILE
# ============================================

@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():

    if "user_id" not in session:

        flash("Please login first.", "warning")

        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    if request.method == "POST":

        fullname = request.form["fullname"]

        email = request.form["email"]

        cursor.execute("""
            UPDATE users
            SET
                fullname=%s,
                email=%s
            WHERE id=%s
        """,
        (
            fullname,
            email,
            user_id
        ))

        conn.commit()

        session["name"] = fullname

        flash(
            "Profile Updated Successfully.",
            "success"
        )

        return redirect(
            url_for("profile.profile")
        )

    cursor.execute("""
        SELECT
            id,
            fullname,
            email,
            created_at
        FROM users
        WHERE id=%s
    """,
    (user_id,)
    )

    user = cursor.fetchone()

    return render_template(
        "profile.html",
        user=user
    )