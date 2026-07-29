import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class DiabetesPreprocessor:

    def __init__(self, filepath):

        self.filepath = filepath

        self.scaler = StandardScaler()

        self.feature_names = []


    def preprocess(self):

        # ---------------- Load Dataset ---------------- #

        df = pd.read_csv(self.filepath)

        # ---------------- Features & Target ---------------- #

        X = df.drop(columns=["Outcome"])

        y = df["Outcome"]

        self.feature_names = list(X.columns)

        # ---------------- Train Test Split ---------------- #

        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,

            test_size=0.20,

            random_state=42,

            stratify=y

        )

        # ---------------- Feature Scaling ---------------- #

        X_train = self.scaler.fit_transform(X_train)

        X_test = self.scaler.transform(X_test)

        return X_train, X_test, y_train, y_test