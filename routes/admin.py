from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from database.db import cursor, conn

admin_bp = Blueprint("admin", __name__)

# -----------------------------
# Admin Credentials
# -----------------------------
ADMIN_EMAIL = "admin@creditai.com"
ADMIN_PASSWORD = "admin123"

# -----------------------------
# Admin Login
# -----------------------------
@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:

            session["admin"] = True
            session["admin_email"] = email

            flash("Admin Login Successful", "success")

            return redirect(url_for("admin.admin_dashboard"))

        flash("Invalid Admin Credentials", "danger")

    return render_template("admin/admin_login.html")


# -----------------------------
# Admin Dashboard
# -----------------------------
@admin_bp.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("admin.admin_login"))

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE status='Approved'")
    approved = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE status='Rejected'")
    rejected = cursor.fetchone()[0]

    return render_template(
        "admin/admin_dashboard.html",
        total_users=total_users,
        total_predictions=total_predictions,
        approved=approved,
        rejected=rejected
    )


# -----------------------------
# All Users
# -----------------------------
@admin_bp.route("/admin/users")
def users():

    if "admin" not in session:
        return redirect(url_for("admin.admin_login"))

    cursor.execute("""
        SELECT
            id,
            fullname,
            email
        FROM users
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    return render_template(
        "admin/users.html",
        users=users
    )


# -----------------------------
# Delete User
# -----------------------------
@admin_bp.route("/admin/delete_user/<int:id>")
def delete_user(id):

    if "admin" not in session:
        return redirect(url_for("admin.admin_login"))

    # Delete user's predictions first
    cursor.execute(
        "DELETE FROM predictions WHERE user_id=%s",
        (id,)
    )

    # Delete user
    cursor.execute(
        "DELETE FROM users WHERE id=%s",
        (id,)
    )

    conn.commit()

    flash("User Deleted Successfully", "success")

    return redirect(url_for("admin.users"))


# -----------------------------
# Prediction History
# -----------------------------
@admin_bp.route("/admin/predictions")
def predictions():

    if "admin" not in session:
        return redirect(url_for("admin.admin_login"))

    cursor.execute("""
        SELECT
            p.id,
            u.fullname,
            p.age,
            p.income,
            p.credit_score,
            p.risk,
            p.status,
            p.created_at
        FROM predictions p
        JOIN users u
        ON p.user_id = u.id
        ORDER BY p.created_at DESC
    """)

    predictions = cursor.fetchall()

    return render_template(
        "admin/predictions.html",
        predictions=predictions
    )


# -----------------------------
# Admin Logout
# -----------------------------
@admin_bp.route("/admin/logout")
def admin_logout():

    session.pop("admin", None)
    session.pop("admin_email", None)

    flash("Admin Logout Successful", "success")

    return redirect(url_for("admin.admin_login"))