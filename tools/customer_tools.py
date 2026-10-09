import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "banking.db"


def get_customer_profile(customer_id: str):
    """Retrieve a customer's profile."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT customer_id, name, age, city, occupation, monthly_income
        FROM customers
        WHERE customer_id = ?
        """,
        (customer_id,)
    )

    customer = cursor.fetchone()
    conn.close()

    if not customer:
        return {
            "success": False,
            "message": f"Customer {customer_id} not found."
        }

    return {
        "success": True,
        "customer": dict(customer)
    }


def get_account_balance(customer_id: str):
    """Retrieve all account balances for a customer."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT account_id, type, balance, status
        FROM accounts
        WHERE customer_id = ?
        """,
        (customer_id,)
    )

    accounts = [dict(row) for row in cursor.fetchall()]
    conn.close()

    if not accounts:
        return {
            "success": False,
            "message": f"No accounts found for {customer_id}."
        }

    return {
        "success": True,
        "accounts": accounts
    }