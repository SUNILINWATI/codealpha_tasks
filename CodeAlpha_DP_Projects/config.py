import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = "DiseasePredictionProject@2026"

    # ---------------- MySQL ---------------- #

    MYSQL_HOST = "127.0.0.1"

    MYSQL_USER = "root"

    MYSQL_PASSWORD = "Sunil@123"

    MYSQL_DB = "disease_prediction"

    MYSQL_CURSORCLASS = "DictCursor"

    # ---------------- Upload Folder ---------------- #

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    # ---------------- Model Folder ---------------- #

    MODEL_FOLDER = os.path.join(
        BASE_DIR,
        "model",
        "saved_models"
    )

    # ---------------- Session ---------------- #

    SESSION_PERMANENT = False

    SESSION_TYPE = "filesystem"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024