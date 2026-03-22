# Customer Churn Prediction System

[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-1.27-green)](https://streamlit.io/)  
[![XGBoost](https://img.shields.io/badge/XGBoost-3.2-orange)](https://xgboost.ai/)  

---

## Project Overview

The **Customer Churn Prediction System** is an end-to-end data science project that predicts whether a customer is likely to leave a service. The system combines **machine learning**, **explainable AI**, **interactive dashboards**, and **database-backed user management** to create a fully functional, real-world application.

The platform allows users to:
- Predict customer churn using **XGBoost**  
- Get insights and actionable recommendations based on prediction  
- Visualize **feature importance** with **SHAP**  
- Track prediction history in **MySQL**  
- Access dashboards with live analytics  

The system supports **user roles**, allowing admins to view all users’ prediction histories while regular users can only see their own.

---

## Key Features

### 1. Login & Role-Based Access
- Secure login system with user credentials  
- Two roles:  
  - `user`: can see only their own prediction history  
  - `admin`: can access all users’ prediction history  

### 2. Interactive Dashboard
- Churn distribution visualization  
- Monthly charges vs churn analysis  
- Tenure and contract type analysis  
- Dynamic charts using **Matplotlib**  

### 3. Customer Churn Prediction
- Predicts churn probability using **XGBoost**  
- Input features include tenure, monthly charges, contract type, internet service, and senior citizen status  
- Provides actionable recommendations based on prediction  

### 4. Explainable AI
- Uses **SHAP** to interpret model predictions  
- Waterfall charts and feature importance plots  

### 5. Database Integration
- **MySQL** backend stores users and prediction history  
- Enables tracking, auditing, and user-specific dashboards  

---

## Tech Stack

- **Python 3.14**  
- **Streamlit** for web interface  
- **XGBoost** for machine learning  
- **SHAP** for explainable AI  
- **Pandas / NumPy** for data processing  
- **Matplotlib** for visualizations  
- **MySQL** for user and prediction storage  

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/shravani370/Customer-Churn-Prediction.git
cd Customer-Churn-Prediction