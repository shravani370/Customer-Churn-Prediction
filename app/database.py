# Dummy database functions for Streamlit deployment (DB disabled)

# ---------------- USER FUNCTIONS ----------------
def add_user(username, password, role="user"):
    # pretend user added successfully
    return True

def login_user(username, password):
    # return dummy login success
    return (username, "user")

# ---------------- PREDICTION FUNCTIONS ----------------
def save_prediction(username, tenure, monthly, total, prediction, prob):
    # do nothing (no DB storage)
    pass

def get_user_history(username):
    # return empty history
    return []

def get_all_history():
    # return empty history
    return []