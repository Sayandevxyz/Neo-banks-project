import random
import mysql.connector
from datetime import datetime, timedelta

# ================== DB ==================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="neobank"
)
cursor = db.cursor()

# ================== OTP ==================
def generate_otp():
    return str(random.randint(100000, 999999))


# ================== LOGIN ==================
def login_user(username, password):
    cursor.execute(
        "SELECT password, login_attempts, is_locked FROM users WHERE username=%s",
        (username,)
    )
    result = cursor.fetchone()

    if not result:
        return {"status": "error", "message": "User not found"}

    stored_password, attempts, is_locked = result

    # LOCK CHECK
    if is_locked:
        return {
            "status": "error",
            "message": "Account locked. Try later."
        }

    # WRONG PASSWORD
    if password != stored_password:
        attempts += 1

        # update attempts
        cursor.execute(
            "UPDATE users SET login_attempts=%s WHERE username=%s",
            (attempts, username)
        )
        db.commit()

        if attempts >= 3:
            cursor.execute(
                "UPDATE users SET is_locked=TRUE WHERE username=%s",
                (username,)
            )
            db.commit()

            return {
                "status": "error",
                "message": "Too many wrong attempts. Account locked."
            }

        return {
            "status": "error",
            "message": f"Incorrect password. Attempts left: {3 - attempts}"
        }

    # CORRECT PASSWORD
    cursor.execute(
        "UPDATE users SET login_attempts=0 WHERE username=%s",
        (username,)
    )
    db.commit()

    otp = generate_otp()
    expiry = datetime.now() + timedelta(minutes=5)

    cursor.execute(
        "UPDATE users SET otp=%s, otp_expiry=%s, otp_resend_count=0 WHERE username=%s",
        (otp, expiry, username)
    )
    db.commit()

    return {
        "status": "success",
        "message": "OTP generated"
    }


# ================== RESEND OTP ==================
def resend_otp(username):
    cursor.execute(
        "SELECT otp_resend_count FROM users WHERE username=%s",
        (username,)
    )
    result = cursor.fetchone()

    if not result:
        return {"status": "error", "message": "User not found"}

    resend_count = result[0]

    if resend_count >= 5:
        return {
            "status": "error",
            "message": "Resend limit reached"
        }

    otp = generate_otp()
    expiry = datetime.now() + timedelta(minutes=5)

    new_count = resend_count + 1

    cursor.execute(
        "UPDATE users SET otp=%s, otp_expiry=%s, otp_resend_count=%s WHERE username=%s",
        (otp, expiry, new_count, username)
    )
    db.commit()

    return {
        "status": "success",
        "message": f"OTP resent ({5 - new_count} left)"
    }


# ================== VERIFY OTP ==================
def verify_otp(username, user_otp):
    cursor.execute(
        "SELECT otp, otp_expiry FROM users WHERE username=%s",
        (username,)
    )
    result = cursor.fetchone()

    if not result:
        return {"status": "error", "message": "User not found"}

    stored_otp, expiry = result

    if datetime.now() > expiry:
        return {"status": "error", "message": "OTP expired"}

    if stored_otp == user_otp:
        return {"status": "success", "message": "Login successful"}

    return {"status": "error", "message": "Invalid OTP"}