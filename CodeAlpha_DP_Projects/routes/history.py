from flask import Blueprint
from flask import render_template
from flask import session
from flask import request
from flask import redirect
from flask import flash

from database.db import mysql
from routes.auth_guard import login_required

history_bp = Blueprint(
    "history_bp",
    __name__
)


@history_bp.route("/history")
@login_required
def history():

    disease = request.args.get("disease")

    cur = mysql.connection.cursor()

    if disease:

        cur.execute("""

            SELECT *

            FROM predictions

            WHERE user_id=%s

            AND disease=%s

            ORDER BY created_at DESC

        """,(

            session["user_id"],

            disease

        ))

    else:

        cur.execute("""

            SELECT *

            FROM predictions

            WHERE user_id=%s

            ORDER BY created_at DESC

        """,(

            session["user_id"],

        ))

    rows = cur.fetchall()

    cur.close()

    return render_template(

        "history.html",

        history=rows

    )


@history_bp.route("/delete_prediction/<int:id>")
@login_required
def delete_prediction(id):

    cur = mysql.connection.cursor()

    cur.execute("""

        DELETE FROM predictions

        WHERE id=%s

        AND user_id=%s

    """,(

        id,

        session["user_id"]

    ))

    mysql.connection.commit()

    cur.close()

    flash(

        "Prediction Deleted Successfully",

        "success"

    )

    return redirect("/history")