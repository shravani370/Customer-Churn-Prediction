import mysql.connector
import streamlit as st

def get_connection():
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"]
    )

conn = get_connection()
cursor = conn.cursor()

# ---------------- USER FUNCTIONS ----------------
def add_user(username, password, role="user"):
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, role)
        )
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    cursor.execute(
        "SELECT username, role FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    return cursor.fetchone()

# ---------------- PREDICTION FUNCTIONS ----------------
def save_prediction(username, tenure, monthly, total, prediction, prob):
    cursor.execute(
        """INSERT INTO predictions 
        (username, tenure, monthly, total, prediction, probability) 
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (username, tenure, monthly, total, prediction, prob)
    )
    conn.commit()

def get_user_history(username):
    cursor.execute(
        "SELECT * FROM predictions WHERE username=%s",
        (username,)
    )
    return cursor.fetchall()

def get_all_history():
    cursor.execute("SELECT * FROM predictions")
    return cursor.fetchall()