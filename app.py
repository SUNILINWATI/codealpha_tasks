from flask import Flask
from extensions import mail
from config import Config

# ===============================
# Blueprints
# ===============================

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.prediction import prediction_bp
from routes.history import history_bp
from routes.profile import profile_bp
from routes.settings import settings_bp
# ===============================
# Flask Mail
# ===============================

from flask_mail import Mail

mail = Mail()


# =====================================================
# CREATE APP
# =====================================================

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # -------------------------
    # Initialize Extensions
    # -------------------------

    mail.init_app(app)

    # -------------------------
    # Register Blueprints
    # -------------------------

    app.register_blueprint(auth_bp)

    app.register_blueprint(dashboard_bp)

    app.register_blueprint(prediction_bp)

    app.register_blueprint(history_bp)
    
    app.register_blueprint(profile_bp)
    
    app.register_blueprint(settings_bp)

    # -------------------------
    # Home
    # -------------------------

    @app.route("/home")

    def home():

        return "Credit AI Loan Prediction System Running Successfully."

    return app


# =====================================================
# MAIN
# =====================================================

app = create_app()

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )