import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "credit_score.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS credit_profiles (
            id               INTEGER  PRIMARY KEY AUTOINCREMENT,
            customer_id      INTEGER  NOT NULL UNIQUE,
            customer_name    TEXT     NOT NULL DEFAULT 'Unknown',
            monthly_income   REAL     NOT NULL,
            existing_loans   INTEGER  NOT NULL DEFAULT 0,
            loan_repaid      INTEGER  NOT NULL DEFAULT 0,
            overdraft_count  INTEGER  NOT NULL DEFAULT 0,
            credit_score     REAL     NOT NULL DEFAULT 0.0,
            risk_category    TEXT     NOT NULL DEFAULT 'Unrated',
            evaluated_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS score_history (
            id           INTEGER  PRIMARY KEY AUTOINCREMENT,
            customer_id  INTEGER  NOT NULL,
            score        REAL     NOT NULL,
            risk_label   TEXT     NOT NULL,
            evaluated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
    print("[DB] Database initialised at:", DB_PATH)


if __name__ == "__main__":
    init_db()
