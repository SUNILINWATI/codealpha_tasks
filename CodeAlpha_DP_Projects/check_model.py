import joblib

model = joblib.load("model/breast_cancer/saved_models/breast_model.pkl")
encoder = joblib.load("model/breast_cancer/saved_models/breast_encoder.pkl")
features = joblib.load("model/breast_cancer/saved_models/breast_features.pkl")

print("=" * 50)

print("MODEL")
print(model)

print("\nCLASSES")
print(encoder.classes_)

print("\nFEATURES")

for i, f in enumerate(features, 1):
    print(i, f)

print("=" * 50)