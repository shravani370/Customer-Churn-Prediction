# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import shap
from database import add_user, login_user, save_prediction, get_user_history, get_all_history

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Customer Churn Predictor", layout="centered")

# ---------------- LOGIN SYSTEM ----------------
def login():
    st.title("🔐 Login / Signup")

    option = st.radio("Select Option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup" and st.button("Create Account"):
        if add_user(username, password):
            st.success("Account created successfully! Login now.")
        else:
            st.error("Username already exists!")

    elif option == "Login" and st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["user"] = user[0]
            st.session_state["role"] = user[1]
        else:
            st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ---------------- LOGOUT ----------------
def logout():
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.experimental_rerun()

st.sidebar.success(f"Welcome {st.session_state['user']} 👋")
logout()

# ---------------- LOAD MODEL ----------------
model = joblib.load("models/model.pkl")
features = joblib.load("models/features.pkl")

# ---------------- SIDEBAR NAVIGATION ----------------
page = st.sidebar.selectbox("📌 Navigation", ["Dashboard", "Prediction"])

# =====================================================
# DASHBOARD PAGE
# =====================================================
if page == "Dashboard":
    st.title("📊 Customer Analytics Dashboard")
    st.markdown("Insights from customer data")

    if st.session_state["role"] == "admin":
        df = pd.DataFrame(get_all_history(), columns=["ID","Username","Tenure","MonthlyCharges","TotalCharges","Prediction","Probability"])
    else:
        df = pd.DataFrame(get_user_history(st.session_state["user"]), columns=["ID","Username","Tenure","MonthlyCharges","TotalCharges","Prediction","Probability"])

    st.dataframe(df)

    # ---------------- CHURN DISTRIBUTION ----------------
    st.subheader("📌 Churn Distribution")
    churn_counts = df["Prediction"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(churn_counts, labels=["No","Yes"], autopct="%1.1f%%")
    st.pyplot(fig)

    # ---------------- MONTHLY CHARGES ----------------
    st.subheader("💰 Monthly Charges vs Churn")
    fig, ax = plt.subplots()
    df.boxplot(column="MonthlyCharges", by="Prediction", ax=ax)
    plt.suptitle("")
    ax.set_title("Monthly Charges by Churn")
    st.pyplot(fig)

    # ---------------- TENURE ----------------
    st.subheader("📆 Tenure Distribution")
    fig, ax = plt.subplots()
    df["Tenure"].hist(bins=20, ax=ax)
    ax.set_title("Customer Tenure")
    st.pyplot(fig)

    # ---------------- GLOBAL FEATURE IMPORTANCE ----------------
    if st.session_state["role"] == "admin" and len(df) > 0:
        st.subheader("📈 Global Feature Impact (SHAP)")

        # Prepare dummy dataset for SHAP
        X_all = df[["Tenure","MonthlyCharges","TotalCharges"]].copy()
        X_all["Contract"] = np.random.randint(0,3,len(X_all))
        X_all["InternetService"] = np.random.randint(0,3,len(X_all))
        X_all["SeniorCitizen"] = np.random.randint(0,2,len(X_all))

        explainer = shap.Explainer(model)
        shap_values_all = explainer(X_all)

        fig, ax = plt.subplots()
        shap.plots.bar(shap_values_all, show=False)
        st.pyplot(fig)

# =====================================================
# PREDICTION PAGE
# =====================================================
elif page == "Prediction":
    st.title("📊 Customer Churn Prediction System")
    st.markdown("Predict churn and get actionable insights")
    st.divider()

    # ---------------- INPUT ----------------
    st.subheader("🧾 Enter Customer Details")
    col1, col2 = st.columns(2)

    with col1:
        tenure = st.slider("Tenure (Months)", 0, 72, 12)
        monthly = st.number_input("Monthly Charges ($)", value=50.0)
        senior = st.selectbox("Senior Citizen", ["No", "Yes"])
    with col2:
        total = st.number_input("Total Charges ($)", value=500.0)
        contract_label = st.selectbox("Contract Type", ["Month-to-month","One year","Two year"])
        internet_label = st.selectbox("Internet Service", ["DSL","Fiber optic","No"])

    # ---------------- ENCODING ----------------
    contract_map = {"Month-to-month":0,"One year":1,"Two year":2}
    internet_map = {"DSL":0,"Fiber optic":1,"No":2}
    senior_map = {"No":0,"Yes":1}

    input_data = {feature:0 for feature in features}
    input_data.update({
        "tenure": tenure,
        "MonthlyCharges": monthly,
        "TotalCharges": total,
        "Contract": contract_map[contract_label],
        "InternetService": internet_map[internet_label],
        "SeniorCitizen": senior_map[senior]
    })
    data = pd.DataFrame([input_data])

    # ---------------- PREDICTION ----------------
    if st.button("🔍 Predict Churn", use_container_width=True):
        prediction = model.predict(data)[0]
        prob = model.predict_proba(data)[0][1]

        # Save to database
        save_prediction(st.session_state["user"], tenure, monthly, total, prediction, prob)

        st.subheader("📊 Prediction Result")
        if prediction == 1:
            st.error(f"⚠️ High Churn Risk ({prob*100:.2f}%)")
        else:
            st.success(f"✅ Low Churn Risk ({prob*100:.2f}%)")

        # ---------------- SHAP ----------------
        st.divider()
        st.subheader("🧠 Why this prediction? (Feature Contribution)")
        explainer = shap.Explainer(model)
        shap_values = explainer(data)

        fig, ax = plt.subplots()
        shap.plots.waterfall(shap_values[0], show=False)
        st.pyplot(fig)

        st.subheader("📈 Feature Importance")
        fig2, ax2 = plt.subplots()
        shap.plots.bar(shap_values, show=False)
        st.pyplot(fig2)

        # ---------------- INSIGHTS ----------------
        st.subheader("💡 Automated Insights")
        feature_importance = pd.DataFrame({
            'feature': data.columns,
            'shap_value': shap_values.values[0]
        }).sort_values(by='shap_value', key=abs, ascending=False)

        for _, row in feature_importance.iterrows():
            feature = row['feature']
            impact = row['shap_value']
            if abs(impact) < 0.01:
                continue
            if feature == "MonthlyCharges":
                if impact > 0: st.write("• High MonthlyCharges → Offer discounts")
                else: st.write("• Low MonthlyCharges → Customer is happy")
            elif feature == "tenure":
                if impact > 0: st.write("• Short tenure → Engage customer")
                else: st.write("• Long tenure → Customer loyalty")
            elif feature == "Contract":
                if impact > 0: st.write("• Month-to-month contract → Promote yearly plan")
                else: st.write("• Long-term contract → Customer stability")
            elif feature == "InternetService":
                if impact > 0: st.write("• Fiber optic → Higher churn → Provide better support")
                else: st.write("• DSL / No → Lower churn → Customer satisfied")
            elif feature == "SeniorCitizen":
                if impact > 0: st.write("• Senior citizen → Higher churn risk → Engage specially")
                else: st.write("• Younger customer → Lower churn risk")

# ---------------- FOOTER ----------------
st.divider()
st.markdown("<center>Built with ❤️ using Machine Learning</center>", unsafe_allow_html=True)