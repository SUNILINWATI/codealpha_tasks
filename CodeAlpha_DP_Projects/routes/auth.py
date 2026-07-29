from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from database.db import mysql

auth_bp = Blueprint("auth_bp", __name__)


# ---------------- Home ---------------- #

@auth_bp.route("/")
def home():

    return render_template("index.html")


# ---------------- Login ---------------- #

@auth_bp.route("/login")
def login():

    return render_template("login.html")


# ---------------- Register ---------------- #

@auth_bp.route("/register")
def register():

    return render_template("register.html")


# ---------------- Register User ---------------- #

@auth_bp.route("/register_user", methods=["POST"])
def register_user():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    age = request.form["age"]
    gender = request.form["gender"]

    cur = mysql.connection.cursor()

    cur.execute(

        "SELECT id FROM users WHERE email=%s",

        (email,)

    )

    user = cur.fetchone()

    if user:

        flash("Email already registered.", "danger")

        cur.close()

        return redirect(url_for("auth_bp.register"))

    hashed_password = generate_password_hash(password)

    cur.execute(

        """

        INSERT INTO users

        (name,email,password,age,gender)

        VALUES(%s,%s,%s,%s,%s)

        """,

        (

            name,

            email,

            hashed_password,

            age,

            gender

        )

    )

    mysql.connection.commit()

    cur.close()

    flash("Registration Successful. Please Login.", "success")

    return redirect(url_for("auth_bp.login"))


# ---------------- Login User ---------------- #

@auth_bp.route("/login_user", methods=["POST"])
def login_user():

    email = request.form["email"]
    password = request.form["password"]

    cur = mysql.connection.cursor()

    cur.execute(

        "SELECT * FROM users WHERE email=%s",

        (email,)

    )

    user = cur.fetchone()

    cur.close()

    if user:

        stored_password = user["password"]

        if check_password_hash(

            stored_password,

            password

        ):

            session["logged_in"] = True
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]

            flash(

                "Welcome " + user["name"],

                "success"

            )

            return redirect("/dashboard")

    flash(

        "Invalid Email or Password",

        "danger"

    )

    return redirect("/login")


# ---------------- Logout ---------------- #

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash(

        "Logged Out Successfully",

        "success"

    )

    return redirect("/")