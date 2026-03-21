import mysql.connector

# ---------------- CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NewStrong@123",
        database="churn_db"
    )

# ---------------- USER FUNCTIONS ----------------
def add_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, "user")
        )

        conn.commit()
        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as e:
        print("Error:", e)
        return False


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

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def get_all_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data