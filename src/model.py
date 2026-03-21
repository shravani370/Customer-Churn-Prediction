# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier 
# from sklearn.metrics import accuracy_score, confusion_matrix

# # Load data
# df = pd.read_csv("data/Telco_Customer_Churn.csv")

# # Basic checks
# print(df.head())
# print(df.info())
# print(df.describe())
# print(df.isnull().sum())

# # ❗ FIX 1: Drop useless column
# df.drop("customerID", axis=1, inplace=True)

# # Target conversion
# df["Churn"] = df["Churn"].apply(lambda x: 1 if x == "Yes" else 0)

# # ❗ FIX 2: Handle categorical data properly
# le = LabelEncoder()
# for col in df.select_dtypes(include="object").columns:
#     df[col] = le.fit_transform(df[col])

# # Split
# X = df.drop("Churn", axis=1)
# Y = df["Churn"]

# # ================= EDA =================

# # Churn count
# plt.figure()
# df["Churn"].value_counts().plot(kind="bar")
# plt.title("Churn vs No Churn")

# # Monthly Charges Distribution
# plt.figure()
# plt.hist(df["MonthlyCharges"])
# plt.title("Monthly Charges Distribution")

# # Tenure vs Churn
# plt.figure()
# plt.hist(df[df["Churn"]==1]["tenure"], alpha=0.5, label="Churn")
# plt.hist(df[df["Churn"]==0]["tenure"], alpha=0.5, label="No Churn")
# plt.legend()

# # ❗ FIX 3: Add important EDA
# # Monthly Charges vs Churn
# plt.figure()
# plt.hist(df[df["Churn"]==1]["MonthlyCharges"], alpha=0.5, label="Churn")
# plt.hist(df[df["Churn"]==0]["MonthlyCharges"], alpha=0.5, label="No Churn")
# plt.legend()
# plt.title("Monthly Charges vs Churn")

# # ================= MODEL =================

# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# # Logistic Regression
# lr = LogisticRegression(max_iter=1000)
# lr.fit(X_train, Y_train)
# lr_pred = lr.predict(X_test)

# # Decision Tree
# dt = DecisionTreeClassifier(max_depth=5)
# dt.fit(X_train, Y_train)
# dt_pred = dt.predict(X_test)

# # ❗ FIX 4: Better Random Forest
# rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
# rf.fit(X_train, Y_train)
# rf_pred = rf.predict(X_test)

# # Evaluation
# print("Logistic:", accuracy_score(Y_test, lr_pred))
# print("Decision Tree:", accuracy_score(Y_test, dt_pred))
# print("Random Forest:", accuracy_score(Y_test, rf_pred))

# # Confusion Matrix (best model)
# cm = confusion_matrix(Y_test, rf_pred)
# print("Confusion Matrix:\n", cm)

# # Feature Importance
# print("Feature Importance:")
# for name, val in zip(X.columns, rf.feature_importances_):
#     print(name, ":", round(val, 3))

# # Sample prediction
# sample = X.iloc[[0]]
# print("Sample Prediction:", rf.predict(sample))

# # Correlation
# print(df.corr())

# plt.show()

# # ================= FINAL INSIGHTS =================
# # 1. Churn is lower than non-churn → dataset is imbalanced
# # 2. Customers with lower tenure are more likely to churn
# # 3. Monthly charges show variation and may influence churn
# # 4. Random Forest performs best due to handling non-linear relationships
# # 5. Key factors affecting churn can be identified using feature importance