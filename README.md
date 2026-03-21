# 📊 Customer Churn Prediction using Machine Learning

## 🚀 Project Overview

This project aims to predict whether a customer will **churn (leave the service)** or not using machine learning techniques. Customer churn prediction is a critical problem in industries like telecom, banking, and subscription-based services, where retaining customers is essential.

---

## 🎯 Objective

* Analyze customer data to identify patterns behind churn
* Build machine learning models to predict churn
* Provide insights to help businesses reduce customer loss

---

## 📂 Dataset

* Dataset: Telco Customer Churn Dataset
* Features include:

  * Customer demographics
  * Account information
  * Services subscribed
  * Monthly charges and tenure

---

## 🧠 Approach

### 🔹 1. Data Preprocessing

* Removed irrelevant columns (e.g., `customerID`)
* Converted categorical data into numerical format using Label Encoding
* Checked and handled missing values

---

### 🔹 2. Exploratory Data Analysis (EDA)

Performed EDA using `matplotlib` to understand data patterns:

* Churn vs Non-Churn distribution
* Monthly charges distribution
* Tenure vs churn relationship
* Monthly charges vs churn comparison

---

### 🔹 3. Model Building

Trained and compared multiple machine learning models:

* Logistic Regression
* Decision Tree Classifier
* Random Forest Classifier

---

### 🔹 4. Model Evaluation

* Accuracy Score
* Confusion Matrix

The **Random Forest model** performed best due to its ability to handle non-linear relationships and reduce overfitting.

---

## 📈 Key Insights

* Customers with **lower tenure** are more likely to churn
* Dataset is **imbalanced**, with fewer churn cases
* Monthly charges show variation and may influence churn
* Feature importance highlights key factors affecting customer decisions

---

## 🧪 Technologies Used

* Python
* Pandas
* Matplotlib
* Scikit-learn

---

## 📊 Results

* Built a predictive model to classify customer churn
* Achieved reliable performance using Random Forest
* Identified important features influencing churn

---

## 🔮 Future Improvements

* Use advanced encoding techniques (One-Hot Encoding)
* Perform hyperparameter tuning
* Apply cross-validation
* Deploy model using Flask or FastAPI

---

## 💡 Conclusion

This project demonstrates how machine learning can be used to **analyze customer behavior and predict churn**, helping businesses take proactive steps to retain customers.

---

## 📌 Author

* Shravani Kharwadkar
# Customer Churn Intelligence System

## 🚀 Overview
An end-to-end machine learning system to predict customer churn and provide actionable retention strategies.

## 🔥 Features
- Churn Prediction using XGBoost
- Explainable AI (SHAP)
- Streamlit Web App
- FastAPI Backend
- Business Recommendation Engine

## 📊 Tech Stack
Python, Scikit-learn, XGBoost, SHAP, Streamlit, FastAPI

## 💡 Business Impact
Helps companies identify high-risk customers and take preventive actions, reducing revenue loss.

## ▶️ Run Project

### Train Model
python src/train.py

### Run App
streamlit run app/app.py

### Run API
uvicorn app.api:app --reload