import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("data/churn.csv")

# Preprocessing
X = df.drop(columns=["Churn"])
y = LabelEncoder().fit_transform(df["Churn"])  # 0/1

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost model
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model and features
joblib.dump(model, "models/model.pkl")
joblib.dump(X.columns.tolist(), "models/features.pkl")