-- =====================================================
-- CREATE DATABASE
-- =====================================================

CREATE DATABASE IF NOT EXISTS credit_ai;

USE credit_ai;

-- =====================================================
-- USERS TABLE
-- =====================================================

CREATE TABLE users (

    id INT AUTO_INCREMENT PRIMARY KEY,

    fullname VARCHAR(100) NOT NULL,

    email VARCHAR(100) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- =====================================================
-- PREDICTIONS TABLE
-- =====================================================

CREATE TABLE predictions (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    fullname VARCHAR(100),

    age INT,

    gender VARCHAR(20),

    education VARCHAR(100),

    annual_income DECIMAL(12,2),

    employment_experience INT,

    home_ownership VARCHAR(50),

    loan_amount DECIMAL(12,2),

    loan_purpose VARCHAR(100),

    interest_rate DECIMAL(5,2),

    loan_percent_income DECIMAL(5,2),

    credit_history_length INT,

    credit_score INT,

    previous_default VARCHAR(10),

    prediction INT,

    status VARCHAR(20),

    risk VARCHAR(30),

    confidence DECIMAL(6,2),

    recommendation TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE CASCADE

);

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX idx_prediction_user
ON predictions(user_id);

CREATE INDEX idx_prediction_status
ON predictions(status);

CREATE INDEX idx_prediction_risk
ON predictions(risk);

-- =====================================================
-- SAMPLE USER
-- Password = admin123
-- (Replace with generated hash if using werkzeug hashing)
-- =====================================================

INSERT INTO users(

fullname,

email,

password

)

VALUES(

'Administrator',

'admin@gmail.com',

'admin123'

);

-- =====================================================
-- CHECK TABLES
-- =====================================================

SHOW TABLES;

DESCRIBE users;

DESCRIBE predictions;