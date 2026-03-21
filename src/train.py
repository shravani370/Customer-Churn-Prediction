import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

from preprocess import load_data, preprocess

# -------------------------------
# 1. Load and preprocess data
# -------------------------------
df = load_data("data/churn.csv")
X, y = preprocess(df)

# -------------------------------
# 2. Train-test split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------
# 3. Model (Optimized XGBoost)
# -------------------------------
model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    random_state=42
)

# Train
model.fit(X_train, y_train)

# -------------------------------
# 4. Evaluation
# -------------------------------
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# -------------------------------
# 5. Save model + feature names
# -------------------------------
joblib.dump(model, "models/model.pkl")
joblib.dump(X.columns.tolist(), "models/features.pkl")

print("\nModel and features saved successfully ✅")