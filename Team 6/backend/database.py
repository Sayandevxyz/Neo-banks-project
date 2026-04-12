# ============================================================
#  database.py
#  Handles all SQLite database operations
#  Team Number : 6
# ============================================================

import sqlite3
import datetime

# database file name
DB_NAME = "neobank.db"


# -------------------------------------------------------
# Connect to database
# -------------------------------------------------------

def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row   # this lets us use column names
    return conn


# -------------------------------------------------------
# Create Tables (run once at start)
# -------------------------------------------------------

def create_tables():

    conn = connect()
    cursor = conn.cursor()

    # users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT    NOT NULL,
            upi_id  TEXT    UNIQUE NOT NULL,
            phone   TEXT    NOT NULL,
            balance REAL    DEFAULT 0.0
        )
    """)

    # transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            txn_id       TEXT    NOT NULL,
            sender_upi   TEXT    NOT NULL,
            receiver_upi TEXT    NOT NULL,
            amount       REAL    NOT NULL,
            timestamp    TEXT    NOT NULL,
            status       TEXT    DEFAULT 'SUCCESS'
        )
    """)

    conn.commit()
    conn.close()
    print("  >> Database tables ready")


# -------------------------------------------------------
# Add Sample Users (for testing)
# -------------------------------------------------------

def add_sample_data():

    # check if sample users already exist
    existing = get_user("sayan@okicici")
    if existing:
        return   # already added, skip

    add_user("sayan", "sayan@okicici", "9876543210", 5000.0)
    add_user("team6",  "team6@ybl",     "9123456789", 2000.0)
    add_user("csbs",   "csbs@okhdfcbank","9988776655", 8000.0)

    print("  >> Sample users added for testing")


# -------------------------------------------------------
# Add a New User
# -------------------------------------------------------

def add_user(name, upi_id, phone, balance):

    conn   = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users (name, upi_id, phone, balance)
    VALUES (?, ?, ?, ?)
""", (name, upi_id, phone, balance))

    conn.commit()
    conn.close()


# -------------------------------------------------------
# Get One User by UPI ID
# -------------------------------------------------------

def get_user(upi_id):

    conn   = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE upi_id = ?", (upi_id,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)   # convert to regular dictionary
    return None


# -------------------------------------------------------
# Get All Users
# -------------------------------------------------------

def get_all_users():

    conn   = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# -------------------------------------------------------
# Do a Transaction (send money)
# Updates balances and saves transaction record
# -------------------------------------------------------

def do_transaction(sender_upi, receiver_upi, amount):

    conn   = connect()
    cursor = conn.cursor()

    # deduct from sender
    cursor.execute("""
        UPDATE users SET balance = balance - ?
        WHERE upi_id = ?
    """, (amount, sender_upi))

    # add to receiver
    cursor.execute("""
        UPDATE users SET balance = balance + ?
        WHERE upi_id = ?
    """, (amount, receiver_upi))

    # generate transaction id
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count  = cursor.fetchone()[0]
    txn_id = "TXN" + str(1000 + count + 1)

    # save transaction record
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    cursor.execute("""
        INSERT INTO transactions (txn_id, sender_upi, receiver_upi, amount, timestamp, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (txn_id, sender_upi, receiver_upi, amount, timestamp, "SUCCESS"))

    conn.commit()
    conn.close()

    return txn_id


# -------------------------------------------------------
# Get Last N Transactions for a User
# -------------------------------------------------------

def get_transactions(upi_id, n):

    conn   = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM transactions
        WHERE sender_upi = ? OR receiver_upi = ?
        ORDER BY id DESC
        LIMIT ?
    """, (upi_id, upi_id, n))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]
