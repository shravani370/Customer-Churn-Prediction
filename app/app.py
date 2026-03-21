import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import shap

from database import add_user, login_user, save_prediction, get_user_history, get_all_history

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Churn Predictor", layout="centered")

# ---------------- LOGIN ----------------
def login():
    st.title("🔐 Login / Signup")

    choice = st.selectbox("Select Option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            if add_user(username, password):
                st.success("Account created! Please login")
            else:
                st.error("User already exists")

    if choice == "Login":
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user[0]
                st.session_state["role"] = user[1]
                st.success(f"Welcome {user[0]} 👋")
                st.rerun()
            else:
                st.error("Invalid credentials")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.success(f"Welcome {st.session_state['user']} 👋")

if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.rerun()

# ---------------- LOAD MODEL ----------------
model = joblib.load("models/model.pkl")
features = joblib.load("models/features.pkl")

# ---------------- NAVIGATION ----------------
page = st.sidebar.selectbox("📌 Navigation", ["Dashboard", "Prediction", "History"])

# =====================================================
# 📊 DASHBOARD
# =====================================================
if page == "Dashboard":

    st.title("📊 Customer Analytics Dashboard")

    df = pd.read_csv("data/churn.csv")

    st.subheader("Churn Distribution")
    fig, ax = plt.subplots()
    df["Churn"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
    st.pyplot(fig)

    st.subheader("Monthly Charges vs Churn")
    fig, ax = plt.subplots()
    df.boxplot(column="MonthlyCharges", by="Churn", ax=ax)
    plt.suptitle("")
    st.pyplot(fig)

# =====================================================
# 🔍 PREDICTION
# =====================================================
elif page == "Prediction":

    st.title("🔍 Churn Prediction")

    tenure = st.slider("Tenure", 0, 72, 12)
    monthly = st.number_input("Monthly Charges", value=50.0)
    total = st.number_input("Total Charges", value=500.0)

    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    internet = st.selectbox("Internet", ["DSL", "Fiber optic", "No"])
    senior = st.selectbox("Senior Citizen", ["No", "Yes"])

    contract_map = {"Month-to-month": 0, "One year": 1, "Two year": 2}
    internet_map = {"DSL": 0, "Fiber optic": 1, "No": 2}
    senior_map = {"No": 0, "Yes": 1}

    input_data = {f: 0 for f in features}

    input_data["tenure"] = tenure
    input_data["MonthlyCharges"] = monthly
    input_data["TotalCharges"] = total
    input_data["Contract"] = contract_map[contract]
    input_data["InternetService"] = internet_map[internet]
    input_data["SeniorCitizen"] = senior_map[senior]

    data = pd.DataFrame([input_data])

    if st.button("Predict"):

        pred = model.predict(data)[0]
        prob = model.predict_proba(data)[0][1]

        # SAVE TO DB
        save_prediction(st.session_state["user"], tenure, monthly, total, int(pred), float(prob))

        if pred == 1:
            st.error(f"High Churn Risk ({prob*100:.2f}%)")
        else:
            st.success(f"Low Churn Risk ({prob*100:.2f}%)")

        # SHAP
        st.subheader("Explanation")
        explainer = shap.Explainer(model)
        shap_values = explainer(data)

        fig, ax = plt.subplots()
        shap.plots.waterfall(shap_values[0], show=False)
        st.pyplot(fig)

# =====================================================
# 📜 HISTORY (ADMIN + USER)
# =====================================================
elif page == "History":

    st.title("📜 Prediction History")

    # ADMIN
    if st.session_state["role"] == "admin":
        st.subheader("👑 Admin - All Users Data")

        history = get_all_history()

    # USER
    else:
        st.subheader("👤 Your Data")

        history = get_user_history(st.session_state["user"])

    if history:
        df = pd.DataFrame(history, columns=[
            "ID", "User", "Tenure", "Monthly", "Total", "Prediction", "Probability"
        ])
        st.dataframe(df)
    else:
        st.info("No data found")

# ---------------- FOOTER ----------------
st.markdown("<center>Built with ❤️ using ML + MySQL</center>", unsafe_allow_html=True)