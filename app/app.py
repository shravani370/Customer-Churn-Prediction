import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import shap
from database import add_user, login_user, save_prediction, get_user_history, get_all_history

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Customer Churn Predictor", layout="wide")

# ---------------- LOGIN SYSTEM ----------------
def login():
    st.title("🔐 Login / Signup")
    option = st.radio("Select Option", ["Login", "Signup"])

    if option == "Signup":
        username = st.text_input("New Username")
        password = st.text_input("Password", type="password")
        if st.button("Create Account"):
            if add_user(username, password):
                st.success("✅ Account created. Please login now.")
            else:
                st.error("❌ Username already exists.")

    elif option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user[0]
                st.session_state["role"] = user[1]
            else:
                st.error("❌ Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

st.sidebar.success(f"Welcome {st.session_state['user']} 👋")

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.experimental_rerun()

# ---------------- LOAD MODEL ----------------
model = joblib.load("models/model.pkl")
features = joblib.load("models/features.pkl")

# ---------------- NAVIGATION ----------------
page = st.sidebar.selectbox("📌 Navigation", ["Dashboard", "Prediction", "History"])

# =====================================================
# DASHBOARD
# =====================================================
if page == "Dashboard":
    st.title("📊 Customer Analytics Dashboard")
    df = pd.read_csv("data/churn.csv")

    st.subheader("Churn Distribution")
    churn_counts = df["Churn"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(churn_counts, labels=["No", "Yes"], autopct="%1.1f%%")
    st.pyplot(fig)

    st.subheader("Monthly Charges vs Churn")
    fig, ax = plt.subplots()
    df.boxplot(column="MonthlyCharges", by="Churn", ax=ax)
    plt.suptitle("")
    st.pyplot(fig)

    st.subheader("Tenure Distribution")
    fig, ax = plt.subplots()
    df["tenure"].hist(bins=20, ax=ax)
    st.pyplot(fig)

# =====================================================
# PREDICTION PAGE
# =====================================================
elif page == "Prediction":
    st.title("🔍 Customer Churn Prediction")

    col1, col2 = st.columns(2)
    with col1:
        tenure = st.slider("Tenure (Months)", 0, 72, 12)
        monthly = st.number_input("Monthly Charges ($)", value=50.0)
        senior = st.selectbox("Senior Citizen", ["No", "Yes"])
    with col2:
        total = st.number_input("Total Charges ($)", value=500.0)
        contract_label = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        internet_label = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

    # ENCODING
    contract_map = {"Month-to-month":0,"One year":1,"Two year":2}
    internet_map = {"DSL":0,"Fiber optic":1,"No":2}
    senior_map = {"No":0,"Yes":1}

    input_data = {feature: 0 for feature in features}
    input_data.update({
        "tenure": tenure,
        "MonthlyCharges": monthly,
        "TotalCharges": total,
        "Contract": contract_map[contract_label],
        "InternetService": internet_map[internet_label],
        "SeniorCitizen": senior_map[senior]
    })
    data = pd.DataFrame([input_data])

    if st.button("Predict Churn"):
        prediction = model.predict(data)[0]
        prob = model.predict_proba(data)[0][1]

        save_prediction(st.session_state["user"], tenure, monthly, total, int(prediction), float(prob))

        if prediction == 1:
            st.error(f"⚠️ High Churn Risk ({prob*100:.2f}%)")
        else:
            st.success(f"✅ Low Churn Risk ({prob*100:.2f}%)")

        # SHAP EXPLAINER
        st.subheader("Feature Importance & Explanation")
        explainer = shap.Explainer(model)
        shap_values = explainer(data)

        st.pyplot(shap.plots.bar(shap_values, show=False).figure)
        st.pyplot(shap.plots.waterfall(shap_values[0], show=False).figure)

# =====================================================
# HISTORY PAGE
# =====================================================
elif page == "History":
    st.title("📜 Prediction History")
    if st.session_state["role"] == "admin":
        history = get_all_history()
    else:
        history = get_user_history(st.session_state["user"])

    if history:
        df_history = pd.DataFrame(history, columns=["ID","Username","Tenure","Monthly","Total","Prediction","Probability"])
        st.dataframe(df_history)
    else:
        st.info("No prediction history found.")