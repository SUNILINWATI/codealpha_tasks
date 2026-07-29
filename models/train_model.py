import os
import sys
import warnings
import joblib
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from models.preprocessing import DataPreprocessor

from sklearn.model_selection import (
    train_test_split,
    cross_val_score
)

from sklearn.linear_model import LogisticRegression

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

print("="*80)
print("        CREDIT AI TRAINING")
print("="*80)

# ==========================================================
# LOAD DATASET
# ==========================================================

processor = DataPreprocessor()

df = processor.load_data(
    "dataset/loan_data.csv"
)

print("Dataset Loaded")

print(df.shape)

# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

duplicates = df.duplicated().sum()

print("Duplicates :", duplicates)

df.drop_duplicates(
    inplace=True
)

# ==========================================================
# REMOVE INVALID DATA
# ==========================================================

df = df[
    (df["person_age"] >= 18) &
    (df["person_age"] <= 80)
]

df = df[
    (df["person_emp_exp"] >= 0) &
    (df["person_emp_exp"] <= 45)
]

df = df[
    (df["credit_score"] >= 300) &
    (df["credit_score"] <= 850)
]

df = df[
    df["loan_amnt"] > 0
]

df = df[
    df["person_income"] > 0
]

print("Shape After Cleaning")

print(df.shape)

# ==========================================================
# HANDLE MISSING VALUES
# ==========================================================

print(df.isnull().sum())

df = processor.preprocess(df)

print("Preprocessing Completed")

# ==========================================================
# TARGET
# ==========================================================

print(df["loan_status"].value_counts())

X = df.drop(
    "loan_status",
    axis=1
)

y = df["loan_status"]

# ==========================================================
# ENCODING
# ==========================================================

X = processor.encode(X)

feature_names = list(X.columns)

joblib.dump(
    feature_names,
    "models/feature_names.pkl"
)

print("Feature Names Saved")

# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

print("Train :", X_train.shape)

print("Test :", X_test.shape)

# ==========================================================
# FEATURE SCALING
# ==========================================================

X_train_scaled = processor.fit_scaler(
    X_train
)

X_test_scaled = processor.transform_scaler(
    X_test
)

processor.save_objects()

print("Scaler Saved")
print("Encoders Saved")
# ==========================================================
# MACHINE LEARNING MODELS
# ==========================================================

models = {

    "Logistic Regression": LogisticRegression(

        max_iter=1000,

        random_state=42,

        class_weight="balanced"

    ),

    "Decision Tree": DecisionTreeClassifier(

        random_state=42,

        max_depth=10,

        min_samples_split=10,

        min_samples_leaf=5

    ),

    "Random Forest": RandomForestClassifier(

        n_estimators=500,

        random_state=42,

        class_weight="balanced",

        max_depth=20,

        min_samples_split=5,

        min_samples_leaf=2,

        n_jobs=-1

    )

}

# ==========================================================
# STORE RESULTS
# ==========================================================

results = []

trained_models = {}

prediction_data = {}

# ==========================================================
# TRAIN MODELS
# ==========================================================

for model_name, model in models.items():

    print("\n" + "=" * 80)

    print("Training :", model_name)

    print("=" * 80)

    if model_name == "Logistic Regression":

        model.fit(

            X_train_scaled,

            y_train

        )

        y_pred = model.predict(

            X_test_scaled

        )

        y_prob = model.predict_proba(

            X_test_scaled

        )[:,1]

        cv = cross_val_score(

            model,

            X_train_scaled,

            y_train,

            cv=5,

            scoring="accuracy"

        ).mean()

    else:

        model.fit(

            X_train,

            y_train

        )

        y_pred = model.predict(

            X_test

        )

        y_prob = model.predict_proba(

            X_test

        )[:,1]

        cv = cross_val_score(

            model,

            X_train,

            y_train,

            cv=5,

            scoring="accuracy"

        ).mean()

    accuracy = accuracy_score(

        y_test,

        y_pred

    )

    precision = precision_score(

        y_test,

        y_pred

    )

    recall = recall_score(

        y_test,

        y_pred

    )

    f1 = f1_score(

        y_test,

        y_pred

    )

    auc = roc_auc_score(

        y_test,

        y_prob

    )

    print()

    print("Accuracy :", round(accuracy,4))

    print("Precision :", round(precision,4))

    print("Recall :", round(recall,4))

    print("F1 :", round(f1,4))

    print("ROC AUC :", round(auc,4))

    print("CV :", round(cv,4))

    print()

    print(

        classification_report(

            y_test,

            y_pred

        )

    )

    results.append({

        "Model": model_name,

        "Accuracy": accuracy,

        "Precision": precision,

        "Recall": recall,

        "F1": f1,

        "ROC": auc,

        "CV": cv

    })

    trained_models[model_name] = model

    prediction_data[model_name] = {

        "prediction": y_pred,

        "probability": y_prob

    }

# ==========================================================
# MODEL COMPARISON
# ==========================================================

comparison = pd.DataFrame(

    results

)

comparison = comparison.sort_values(

    by="Accuracy",

    ascending=False

)

print("\n")

print("="*80)

print("MODEL COMPARISON")

print("="*80)

print(comparison)

# ==========================================================
# BEST MODEL
# ==========================================================

best_model_name = comparison.iloc[0]["Model"]

best_model = trained_models[best_model_name]

print()

print("="*80)

print("BEST MODEL :", best_model_name)

print("="*80)
# ==========================================================
# SAVE BEST MODEL
# ==========================================================

joblib.dump(
    best_model,
    "models/best_model.pkl"
)

print("\n✅ Best Model Saved")

# ==========================================================
# SAVE MODEL COMPARISON
# ==========================================================

comparison.to_csv(
    "models/model_comparison.csv",
    index=False
)

print("✅ Model Comparison Saved")

# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================

if hasattr(best_model, "feature_importances_"):

    importance = pd.DataFrame({

        "Feature": feature_names,

        "Importance": best_model.feature_importances_

    })

    importance = importance.sort_values(

        by="Importance",

        ascending=False

    )

    print("\n")

    print("="*80)

    print("TOP IMPORTANT FEATURES")

    print("="*80)

    print(importance.head(15))

    importance.to_csv(

        "models/feature_importance.csv",

        index=False

    )

# ==========================================================
# CONFUSION MATRIX
# ==========================================================

best_prediction = prediction_data[
    best_model_name
]["prediction"]

cm = confusion_matrix(

    y_test,

    best_prediction

)

print("\n")

print("="*80)

print("CONFUSION MATRIX")

print("="*80)

print(cm)

# ==========================================================
# CLASSIFICATION REPORT
# ==========================================================

print("\n")

print("="*80)

print("FINAL CLASSIFICATION REPORT")

print("="*80)

print(

    classification_report(

        y_test,

        best_prediction

    )

)

