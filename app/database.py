import streamlit as st
import mysql.connector

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    conn = mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"]
    )
    return conn

# ---------------- USER FUNCTIONS ----------------
def add_user(username, password, role="user"):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, role)
        )
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, role FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# ---------------- PREDICTION FUNCTIONS ----------------
def save_prediction(username, tenure, monthly, total, prediction, prob):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO predictions 
        (username, tenure, monthly, total, prediction, probability) 
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (username, tenure, monthly, total, prediction, prob)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_user_history(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM predictions WHERE username=%s",
        (username,)
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_all_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result