import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET = os.path.join(BASE_DIR, "..", "..", "dataset", "diabetes.csv")
SAVE_DIR = os.path.join(BASE_DIR, "saved_models")

os.makedirs(SAVE_DIR, exist_ok=True)

# ---------------- Dataset ---------------- #

df = pd.read_csv(DATASET)

X = df.drop("Outcome", axis=1)
y = df["Outcome"]

feature_names = list(X.columns)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------------- Scaling ---------------- #

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---------------- Logistic Regression ---------------- #

lr = LogisticRegression(
    max_iter=1000,
    random_state=42
)

lr.fit(X_train_scaled, y_train)

lr_pred = lr.predict(X_test_scaled)

lr_acc = accuracy_score(y_test, lr_pred)
lr_pre = precision_score(y_test, lr_pred)
lr_rec = recall_score(y_test, lr_pred)
lr_f1 = f1_score(y_test, lr_pred)

print("\n===== Logistic Regression =====")
print("Accuracy :", round(lr_acc*100,2))
print("Precision:", round(lr_pre*100,2))
print("Recall   :", round(lr_rec*100,2))
print("F1 Score :", round(lr_f1*100,2))

# ---------------- Random Forest ---------------- #

rf = RandomForestClassifier(
    n_estimators=500,
    max_depth=15,
    class_weight="balanced",
    random_state=42
)

rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)

rf_acc = accuracy_score(y_test, rf_pred)
rf_pre = precision_score(y_test, rf_pred)
rf_rec = recall_score(y_test, rf_pred)
rf_f1 = f1_score(y_test, rf_pred)

print("\n===== Random Forest =====")
print("Accuracy :", round(rf_acc*100,2))
print("Precision:", round(rf_pre*100,2))
print("Recall   :", round(rf_rec*100,2))
print("F1 Score :", round(rf_f1*100,2))

# ---------------- Best Model ---------------- #

if lr_f1 >= rf_f1:

    best_model = lr
    best_name = "Logistic Regression"
    use_scaler = True

else:

    best_model = rf
    best_name = "Random Forest"
    use_scaler = False

joblib.dump(best_model,
            os.path.join(SAVE_DIR,"diabetes_model.pkl"))

joblib.dump(feature_names,
            os.path.join(SAVE_DIR,"diabetes_features.pkl"))

joblib.dump(scaler,
            os.path.join(SAVE_DIR,"diabetes_scaler.pkl"))

joblib.dump(use_scaler,
            os.path.join(SAVE_DIR,"use_scaler.pkl"))

print("\nBest Model :",best_name)
print("Model Saved Successfully")