from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    request
)

from werkzeug.security import generate_password_hash, check_password_hash

from database.db import cursor, conn


settings_bp = Blueprint(
    "settings",
    __name__
)


# =====================================================
# SETTINGS
# =====================================================

@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():

    if "user_id" not in session:

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    user_id = session["user_id"]

    cursor.execute("""

        SELECT

            fullname,
            email,
            password

        FROM users

        WHERE id=%s

    """, (user_id,))

    user = cursor.fetchone()

    if request.method == "POST":

        current_password = request.form["current_password"]

        new_password = request.form["new_password"]

        confirm_password = request.form["confirm_password"]

        if not check_password_hash(
            user[2],
            current_password
        ):

            flash(
                "Current password is incorrect.",
                "danger"
            )

            return redirect(
                url_for("settings.settings")
            )

        if new_password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("settings.settings")
            )

        hashed_password = generate_password_hash(
            new_password
        )

        cursor.execute("""

            UPDATE users

            SET password=%s

            WHERE id=%s

        """,
        (
            hashed_password,
            user_id
        ))

        conn.commit()

        flash(
            "Password Updated Successfully.",
            "success"
        )

        return redirect(
            url_for("settings.settings")
        )

    return render_template(

        "settings.html",

        user=user

    )