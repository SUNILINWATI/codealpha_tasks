from flask import Flask
from config import Config
from database.db import mysql

# ---------------- Create App ---------------- #
app = Flask(__name__)
app.config.from_object(Config)

# ---------------- Initialize Extensions ---------------- #
mysql.init_app(app)

# ---------------- Import Blueprints ---------------- #
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.history import history_bp
from routes.profile import profile_bp
from routes.admin import admin_bp
from routes.heart_disease import heart_bp
from routes.diabetes import diabetes_bp
from routes.breast_cancer import breast_bp
from routes.report import report_bp
from routes.settings import settings_bp
  
# ---------------- Register Blueprints ---------------- #
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(history_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(heart_bp)
app.register_blueprint(diabetes_bp)
app.register_blueprint(breast_bp)
app.register_blueprint(report_bp)
app.register_blueprint(settings_bp)

# ---------------- Error Pages ---------------- #
@app.errorhandler(404)
def page_not_found(error):
    return "<h2>404 - Page Not Found</h2>", 404


@app.errorhandler(500)
def internal_server_error(error):
    return "<h2>500 - Internal Server Error</h2>", 500


# ---------------- Run App ---------------- #
if __name__ == "__main__":
    app.run(debug=True)