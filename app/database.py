import mysql.connector
from mysql.connector import Error

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",       # change if using remote DB
            user="root",            # your MySQL username
            password="NewStrong@123",  # your MySQL password
            database="churn_db"     # make sure DB exists
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

# ---------------- USER FUNCTIONS ----------------
def add_user(username, password, role="user"):
    conn = get_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, role)
        )
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Add user error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT username, role FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(f"Login error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# ---------------- PREDICTION FUNCTIONS ----------------
def save_prediction(username, tenure, monthly, total, prediction, prob):
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO predictions
            (username, tenure, monthly, total, prediction, probability)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (username, tenure, monthly, total, prediction, prob)
        )
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Save prediction error: {e}")
    finally:
        cursor.close()
        conn.close()

def get_user_history(username):
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM predictions WHERE username=%s",
            (username,)
        )
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Get user history error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_all_history():
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM predictions")
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Get all history error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()