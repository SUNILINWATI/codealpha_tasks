CREATE DATABASE disease_prediction;

USE disease_prediction;

CREATE TABLE users(

id INT PRIMARY KEY AUTO_INCREMENT,

name VARCHAR(100),

email VARCHAR(100) UNIQUE,

password VARCHAR(255),

age INT,

gender VARCHAR(20),

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

DROP TABLE IF EXISTS predictions;

CREATE TABLE predictions(

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,

    patient_name VARCHAR(100),

    disease VARCHAR(100),

    prediction INT,

    probability FLOAT,

    risk_level VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id) REFERENCES users(id)

);
CREATE TABLE admin(

id INT PRIMARY KEY AUTO_INCREMENT,

username VARCHAR(50),

password VARCHAR(255)

);