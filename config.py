class Config:

    # ==========================
    # Flask
    # ==========================

    SECRET_KEY = "your-secret-key"

    # ==========================
    # MySQL
    # ==========================

    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "Sunil@123"
    MYSQL_DATABASE = "loan_prediction"

    # ==========================
    # Flask Mail
    # ==========================

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME = "your_email@gmail.com"
    MAIL_PASSWORD = "your_16_digit_app_password"

    MAIL_DEFAULT_SENDER = "your_email@gmail.com"