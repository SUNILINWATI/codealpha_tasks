import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder


class DataPreprocessor:

    def __init__(self, filepath):

        self.filepath = filepath
        self.scaler = StandardScaler()
        self.feature_names = []

    def preprocess(self):

        df = pd.read_csv(self.filepath)

        # Target Column
        y = df["has_heart_disease"]

        # Only Important Features
        selected_features = [

            "age",
            "sex",
            "resting_bp_systolic",
            "resting_bp_diastolic",
            "cholesterol_total",
            "fasting_blood_sugar",
            "bmi",
            "resting_heart_rate",
            "chest_pain_type",
            "exercise_induced_angina",
            "st_depression",
            "family_history",
            "smoker_status"

        ]

        X = df[selected_features]

        self.feature_names = selected_features

        # Encode Categorical Columns
        categorical_columns = [

            "sex",
            "chest_pain_type",
            "exercise_induced_angina",
            "family_history",
            "smoker_status"

        ]

        for col in categorical_columns:

            encoder = LabelEncoder()
            X[col] = encoder.fit_transform(X[col])

        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y

        )

        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)

        return X_train, X_test, y_train, y_test