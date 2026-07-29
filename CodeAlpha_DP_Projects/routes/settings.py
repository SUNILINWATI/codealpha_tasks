from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import flash
from flask import redirect
from flask import url_for

from database.db import mysql
from routes.auth_guard import login_required

settings_bp = Blueprint(
    "settings_bp",
    __name__
)


@settings_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT
        name,
        email,
        password
    FROM users
    WHERE id=%s
    """, (session["user_id"],))
    
    user = cur.fetchone()

    if request.method == "POST":

        flash("Settings Saved Successfully!", "success")

        return redirect(url_for("settings_bp.settings"))

    return render_template(

        "settings.html",

        username=user["name"],

        email=user["email"]

    )