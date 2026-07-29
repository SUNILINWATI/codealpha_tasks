import os
import joblib
import warnings

warnings.filterwarnings("ignore")

from preprocess import BreastCancerPreprocessor

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

import pandas as pd

df = pd.read_csv("../../dataset/breast_cancer.csv")

print(df.columns.tolist())
# -----------------------------
# Paths
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET = os.path.join(
    BASE_DIR,
    "..",
    "..",
    "dataset",
    "breast_cancer.csv"
)

SAVE_DIR = os.path.join(
    BASE_DIR,
    "saved_models"
)

os.makedirs(SAVE_DIR, exist_ok=True)

# -----------------------------
# Load Dataset
# -----------------------------

processor = BreastCancerPreprocessor(DATASET)

X_train, X_test, y_train, y_test = processor.preprocess()

# -----------------------------
# Models
# -----------------------------

models = {

    "Logistic Regression":
        LogisticRegression(max_iter=1000),

    "Decision Tree":
        DecisionTreeClassifier(random_state=42),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=300,
            random_state=42
        ),

    "Gradient Boosting":
        GradientBoostingClassifier(
            random_state=42
        )

}

best_model = None
best_accuracy = 0
best_name = ""

print("=" * 60)
print(" BREAST CANCER MODEL TRAINING ")
print("=" * 60)

for name, model in models.items():

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    accuracy = accuracy_score(y_test, prediction)

    precision = precision_score(y_test, prediction)

    recall = recall_score(y_test, prediction)

    f1 = f1_score(y_test, prediction)

    print()
    print(name)
    print("-" * 40)
    print("Accuracy :", round(accuracy * 100, 2), "%")
    print("Precision:", round(precision * 100, 2), "%")
    print("Recall   :", round(recall * 100, 2), "%")
    print("F1 Score :", round(f1 * 100, 2), "%")

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_model = model

        best_name = name

# -----------------------------
# Save Files
# -----------------------------

joblib.dump(
    best_model,
    os.path.join(
        SAVE_DIR,
        "breast_model.pkl"
    )
)

joblib.dump(
    processor.scaler,
    os.path.join(
        SAVE_DIR,
        "breast_scaler.pkl"
    )
)

joblib.dump(
    processor.feature_names,
    os.path.join(
        SAVE_DIR,
        "breast_features.pkl"
    )
)

joblib.dump(
    processor.encoder,
    os.path.join(
        SAVE_DIR,
        "breast_encoder.pkl"
    )
)

print()
print("=" * 60)
print("Best Model :", best_name)
print("Accuracy   :", round(best_accuracy * 100, 2), "%")
print("Model Saved Successfully")
print("=" * 60)