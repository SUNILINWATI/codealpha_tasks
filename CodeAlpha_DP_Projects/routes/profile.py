from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import session

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from database.db import mysql
from routes.auth_guard import login_required

profile_bp = Blueprint(
    "profile_bp",
    __name__
)


@profile_bp.route("/profile")
@login_required
def profile():

    cur = mysql.connection.cursor()

    cur.execute("""

        SELECT *

        FROM users

        WHERE id=%s

    """,(

        session["user_id"],

    ))

    user = cur.fetchone()

    cur.close()

    return render_template(

        "profile.html",

        user=user

    )


@profile_bp.route("/update_profile", methods=["POST"])
@login_required
def update_profile():

    name = request.form["name"]
    age = request.form["age"]
    gender = request.form["gender"]

    cur = mysql.connection.cursor()

    cur.execute("""

        UPDATE users

        SET

        name=%s,

        age=%s,

        gender=%s

        WHERE id=%s

    """,(

        name,

        age,

        gender,

        session["user_id"]

    ))

    mysql.connection.commit()

    cur.close()

    session["user_name"] = name

    flash(

        "Profile Updated Successfully",

        "success"

    )

    return redirect("/profile")


@profile_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():

    current = request.form["current_password"]

    new = request.form["new_password"]

    cur = mysql.connection.cursor()

    cur.execute(

        "SELECT password FROM users WHERE id=%s",

        (

            session["user_id"],

        )

    )

    user = cur.fetchone()

    if not check_password_hash(

        user["password"],

        current

    ):

        flash(

            "Current Password is incorrect",

            "danger"

        )

        cur.close()

        return redirect("/profile")

    password = generate_password_hash(new)

    cur.execute("""

        UPDATE users

        SET password=%s

        WHERE id=%s

    """,(

        password,

        session["user_id"]

    ))

    mysql.connection.commit()

    cur.close()

    flash(

        "Password Changed Successfully",

        "success"

    )

    return redirect("/profile")