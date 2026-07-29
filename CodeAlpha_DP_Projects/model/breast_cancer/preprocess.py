import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder


class BreastCancerPreprocessor:

    def __init__(self, filepath):
        self.filepath = filepath
        self.scaler = StandardScaler()
        self.encoder = LabelEncoder()
        self.feature_names = []

    def preprocess(self):

        # Load dataset
        df = pd.read_csv(self.filepath)

        # Replace spaces with underscores
        df.columns = df.columns.str.replace(" ", "_")

        # Remove ID column if present
        if "id" in df.columns:
            df.drop("id", axis=1, inplace=True)

        # Remove unnamed column if present
        if "Unnamed:_32" in df.columns:
            df.drop("Unnamed:_32", axis=1, inplace=True)

        # Encode target column
        y = self.encoder.fit_transform(df["diagnosis"])

        # Selected features
        selected_features = [
            "radius_mean",
            "texture_mean",
            "perimeter_mean",
            "area_mean",
            "smoothness_mean",
            "compactness_mean",
            "concavity_mean",
            "concave_points_mean",
            "symmetry_mean",
            "radius_worst",
            "texture_worst",
            "perimeter_worst",
            "area_worst",
            "concave_points_worst",
            "fractal_dimension_worst"
        ]

        # Features
        X = df[selected_features]

        # Save feature names
        self.feature_names = selected_features

        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        # Feature scaling
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)

        return X_train, X_test, y_train, y_test