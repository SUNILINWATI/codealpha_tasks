import os
import joblib
import warnings

warnings.filterwarnings("ignore")

from preprocess import DataPreprocessor

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ---------------- Paths ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "..",
        "dataset",
        "heart_disease.csv"
    )
)

SAVE_DIR = os.path.join(
    BASE_DIR,
    "saved_models"
)

os.makedirs(SAVE_DIR, exist_ok=True)

# ---------------- Load Dataset ---------------- #

processor = DataPreprocessor(DATASET)

X_train, X_test, y_train, y_test = processor.preprocess()

# ---------------- Model ---------------- #

model = RandomForestClassifier(

    n_estimators=500,

    max_depth=10,

    min_samples_split=5,

    min_samples_leaf=2,

    random_state=42

)

print("=" * 60)
print(" HEART DISEASE MODEL TRAINING ")
print("=" * 60)

# ---------------- Train ---------------- #

model.fit(X_train, y_train)

prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)
precision = precision_score(y_test, prediction)
recall = recall_score(y_test, prediction)
f1 = f1_score(y_test, prediction)

print("\nRandom Forest")
print("-" * 40)
print("Accuracy :", round(accuracy * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall   :", round(recall * 100, 2), "%")
print("F1 Score :", round(f1 * 100, 2), "%")

# ---------------- Save ---------------- #

joblib.dump(
    model,
    os.path.join(
        SAVE_DIR,
        "heart_model.pkl"
    )
)

joblib.dump(
    processor.scaler,
    os.path.join(
        SAVE_DIR,
        "heart_scaler.pkl"
    )
)

joblib.dump(
    processor.feature_names,
    os.path.join(
        SAVE_DIR,
        "heart_features.pkl"
    )
)

print("\nSelected Features\n")

for i, feature in enumerate(processor.feature_names, start=1):
    print(f"{i}. {feature}")

print()
print("=" * 60)
print("Model : Random Forest")
print("Accuracy :", round(accuracy * 100, 2), "%")
print("Model Saved Successfully")
print("=" * 60)