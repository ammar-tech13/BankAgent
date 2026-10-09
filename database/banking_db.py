import sqlite3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "banking.db"
DATA_DIR = ROOT / "data"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        city TEXT,
        occupation TEXT,
        monthly_income REAL,
        phone TEXT
    );

    CREATE TABLE IF NOT EXISTS accounts (
        account_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        type TEXT,
        balance REAL,
        status TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id TEXT PRIMARY KEY,
        account_id TEXT NOT NULL,
        merchant TEXT,
        amount REAL,
        transaction_type TEXT,
        location TEXT,
        status TEXT,
        risk_score REAL,
        FOREIGN KEY(account_id) REFERENCES accounts(account_id)
    );

    CREATE TABLE IF NOT EXISTS loans (
        loan_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        loan_type TEXT,
        principal REAL,
        outstanding REAL,
        monthly_emi REAL,
        status TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE IF NOT EXISTS credit (
        customer_id TEXT PRIMARY KEY,
        credit_score INTEGER,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );
    """)

    # Seed only when the tables are empty.
    if cur.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 0:
        for filename, table in [
            ("customers.json", "customers"),
            ("accounts.json", "accounts"),
            ("transactions.json", "transactions"),
            ("loans.json", "loans"),
            ("credit.json", "credit"),
        ]:
            rows = json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))
            if rows:
                columns = list(rows[0].keys())
                placeholders = ",".join(["?"] * len(columns))
                sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
                cur.executemany(sql, [[row[c] for c in columns] for row in rows])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print(f"Banking database initialized: {DB_PATH}")
