import joblib
import pandas as pd

from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler
)


class DataPreprocessor:

    def __init__(self):

        self.encoders = {}

        self.scaler = StandardScaler()

    # =====================================================
    # LOAD DATA
    # =====================================================

    def load_data(self, path):

        return pd.read_csv(path)

    # =====================================================
    # CLEAN DATA
    # =====================================================

    def preprocess(self, df):

        # Remove duplicates
        df = df.drop_duplicates()

        # Remove missing values
        df = df.dropna()

        # Age
        df = df[
            (df["person_age"] >= 18) &
            (df["person_age"] <= 80)
        ]

        # Experience
        df = df[
            (df["person_emp_exp"] >= 0) &
            (df["person_emp_exp"] <= 45)
        ]

        # Credit Score
        df = df[
            (df["credit_score"] >= 300) &
            (df["credit_score"] <= 850)
        ]

        # Income
        df = df[
            df["person_income"] > 0
        ]

        # Loan
        df = df[
            df["loan_amnt"] > 0
        ]

        df.reset_index(
            drop=True,
            inplace=True
        )

        return df

    # =====================================================
    # ENCODE
    # =====================================================

    def encode(self, X):

        categorical = X.select_dtypes(
            include=["object"]
        ).columns

        for col in categorical:

            encoder = LabelEncoder()

            X[col] = encoder.fit_transform(
                X[col].astype(str)
            )

            self.encoders[col] = encoder

        return X

    # =====================================================
    # SCALER
    # =====================================================

    def fit_scaler(self, X):

        return self.scaler.fit_transform(X)

    def transform_scaler(self, X):

        return self.scaler.transform(X)

    # =====================================================
    # SAVE
    # =====================================================

    def save_objects(self):

        joblib.dump(

            self.scaler,

            "models/scaler.pkl"

        )

        joblib.dump(

            self.encoders,

            "models/encoders.pkl"

        )