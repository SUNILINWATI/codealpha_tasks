# CreditAI - AI Based Credit Scoring System

## Project Title

CreditAI is an AI-powered Credit Scoring System developed using Flask, Machine Learning, and MySQL. The system predicts whether a loan applicant is eligible for a loan based on financial and personal details. It also calculates an AI Credit Score, Risk Level, and Recommendation.

---

## Features

- User Registration & Login
- Forgot Password using Email OTP
- User Profile Management
- AI-Based Credit Prediction
- AI Credit Score (300–850)
- Loan Approval / Rejection
- Risk Level Detection
- Prediction History
- Analytics Dashboard
- Admin Login
- MySQL Database Integration
- Responsive User Interface

---

## Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

### Backend
- Python
- Flask

### Database
- MySQL

### Machine Learning
- Scikit-learn
- Random Forest
- Logistic Regression
- Decision Tree

### Libraries
- Pandas
- NumPy
- Matplotlib
- Joblib
- Flask-Mail
- MySQL Connector

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/CreditAI.git
cd CreditAI
```

### Install Requirements

```bash
pip install -r requirements.txt
```

### Configure Database

- Create MySQL Database

```sql
CREATE DATABASE loan_prediction;
```

- Update database credentials in `config.py`

### Run Project

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## Screenshots

Add screenshots of the following pages:

- Login Page
- Dashboard
- Credit Prediction
- AI Prediction Result
- History
- Analytics
- Profile
- Settings

---

## Dataset

Dataset contains information such as:

- Age
- Gender
- Education
- Annual Income
- Employment Experience
- Home Ownership
- Loan Amount
- Loan Purpose
- Interest Rate
- Loan Percentage Income
- Credit History Length
- Credit Score
- Previous Loan Default
- Loan Status

---

## Machine Learning Models

The project compares multiple machine learning algorithms:

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier

Evaluation Metrics:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Cross Validation Score

Random Forest is selected as the final model based on performance.

---

## Accuracy

Model Evaluation includes:

- Accuracy Score
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix
- Classification Report

---

## Future Improvements

- Explainable AI (XAI)
- Loan EMI Calculator
- PDF Report Download
- SMS Notification
- Live Credit Bureau API Integration
- Dark Mode
- Multi-language Support
- Cloud Deployment

---

## Project Structure

```
CreditAI/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── database/
├── dataset/
├── models/
├── routes/
├── static/
└── templates/
```

---

## Author

**Sunil Inwati**

B.Tech Student

CodeAlpha Machine Learning Internship Project

2026