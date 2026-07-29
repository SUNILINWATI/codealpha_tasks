from functools import wraps
from flask import session
from flask import redirect
from flask import url_for
from flask import flash


def login_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if "logged_in" not in session:

            flash(

                "Please login first.",

                "warning"

            )

            return redirect(

                url_for("auth_bp.login")

            )

        return function(*args, **kwargs)

    return decorated_function