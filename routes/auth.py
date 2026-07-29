import random

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_mail import Message

from extensions import mail

from forms import RegistrationForm

from database.db import conn, cursor

auth_bp = Blueprint(
    "auth",
    __name__
)

# ==========================================================
# HOME
# ==========================================================

@auth_bp.route("/")
def home():

    return redirect(
        url_for("auth.login")
    )


# ==========================================================
# REGISTER
# ==========================================================

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        fullname = form.fullname.data.strip()

        email = form.email.data.strip().lower()

        password = form.password.data

        # -------------------------------------
        # CHECK EMAIL
        # -------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user:

            flash(
                "Email already registered.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        # -------------------------------------
        # HASH PASSWORD
        # -------------------------------------

        hashed_password = generate_password_hash(
            password
        )

        # -------------------------------------
        # INSERT USER
        # -------------------------------------

        cursor.execute(
            """
            INSERT INTO users
            (
                fullname,
                email,
                password
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                fullname,
                email,
                hashed_password
            )
        )

        conn.commit()

        flash(
            "Registration Successful. Please Login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html",
        form=form
    )
    
    # ==========================================================
# LOGIN
# ==========================================================

@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # Already Logged In
    if "user_id" in session:

        return redirect(
            url_for("dashboard.dashboard")
        )

    if request.method == "POST":

        email = request.form.get(
            "email"
        ).strip().lower()

        password = request.form.get(
            "password"
        )

        # -----------------------------------
        # CHECK USER
        # -----------------------------------

        cursor.execute(
            """
            SELECT
                id,
                fullname,
                email,
                password
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cursor.fetchone()

        # -----------------------------------
        # INVALID EMAIL
        # -----------------------------------

        if user is None:

            flash(
                "Email not registered.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        # -----------------------------------
        # PASSWORD CHECK
        # -----------------------------------

        if not check_password_hash(
            user[3],
            password
        ):

            flash(
                "Incorrect password.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        # -----------------------------------
        # CREATE SESSION
        # -----------------------------------

        session.clear()

        session["user_id"] = user[0]

        session["name"] = user[1]

        session["email"] = user[2]

        flash(
            f"Welcome {user[1]}!",
            "success"
        )

        print("=" * 60)
        print("LOGIN SUCCESS")
        print("User ID :", user[0])
        print("Name    :", user[1])
        print("Email   :", user[2])
        print("=" * 60)

        return redirect(
            url_for("dashboard.dashboard")
        )

    return render_template(
        "login.html"
    )


# ==========================================================
# LOGOUT
# ==========================================================

@auth_bp.route("/logout")
def logout():

    if "user_id" in session:

        print("=" * 60)
        print("LOGOUT")
        print("User :", session.get("name"))
        print("=" * 60)

    session.clear()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )
    
    # ==========================================================
# FORGOT PASSWORD
# ==========================================================

@auth_bp.route(
    "/forgot_password",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "POST":

        email = request.form.get(
            "email"
        ).strip().lower()

        # ---------------------------------------
        # CHECK EMAIL
        # ---------------------------------------

        cursor.execute(
            """
            SELECT id, fullname
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user is None:

            flash(
                "Email not found.",
                "danger"
            )

            return redirect(
                url_for("auth.forgot_password")
            )

        # ---------------------------------------
        # GENERATE OTP
        # ---------------------------------------

        otp = random.randint(
            100000,
            999999
        )

        # Save OTP in Session

        session["reset_email"] = email

        session["reset_otp"] = str(otp)

        # ---------------------------------------
        # SEND EMAIL
        # ---------------------------------------

        msg = Message(

            subject="Credit AI Password Reset OTP",

            recipients=[email]

        )

        msg.body = f"""
Hello {user[1]},

Your One Time Password (OTP) for resetting your Credit AI account password is:

OTP : {otp}

This OTP is valid only for this password reset request.

If you did not request this, please ignore this email.

----------------------------------------
Credit AI
Loan Prediction System
----------------------------------------
"""

        try:

            mail.send(msg)

            print("=" * 60)
            print("OTP SENT")
            print("Email :", email)
            print("OTP :", otp)
            print("=" * 60)

            flash(
                "OTP sent successfully to your email.",
                "success"
            )

            return redirect(
                url_for("auth.verify_otp")
            )

        except Exception as e:

            print(e)

            flash(
                "Unable to send OTP email.",
                "danger"
            )

            return redirect(
                url_for("auth.forgot_password")
            )

    return render_template(
        "forgot_password.html"
    )
    
    # ==========================================================
# VERIFY OTP
# ==========================================================

@auth_bp.route(
    "/verify_otp",
    methods=["GET", "POST"]
)
def verify_otp():

    if "reset_email" not in session:

        flash(
            "Password reset session expired.",
            "warning"
        )

        return redirect(
            url_for("auth.forgot_password")
        )

    if request.method == "POST":

        entered_otp = request.form.get(
            "otp"
        ).strip()

        saved_otp = session.get(
            "reset_otp"
        )

        if entered_otp == saved_otp:

            flash(
                "OTP Verified Successfully.",
                "success"
            )

            return redirect(
                url_for("auth.reset_password")
            )

        flash(
            "Invalid OTP.",
            "danger"
        )

        return redirect(
            url_for("auth.verify_otp")
        )

    return render_template(
        "verify_otp.html"
    )


# ==========================================================
# RESET PASSWORD
# ==========================================================

@auth_bp.route(
    "/reset_password",
    methods=["GET", "POST"]
)
def reset_password():

    if "reset_email" not in session:

        flash(
            "Password reset session expired.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    if request.method == "POST":

        password = request.form.get(
            "password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("auth.reset_password")
            )

        hashed_password = generate_password_hash(
            password
        )

        cursor.execute(
            """
            UPDATE users
            SET password=%s
            WHERE email=%s
            """,
            (
                hashed_password,
                session["reset_email"]
            )
        )

        conn.commit()

        print("=" * 60)
        print("PASSWORD RESET SUCCESS")
        print("Email :", session["reset_email"])
        print("=" * 60)

        # Clear Reset Session

        session.pop("reset_email", None)

        session.pop("reset_otp", None)

        flash(
            "Password Reset Successfully. Please Login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "reset_password.html"
    )