import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "banking.db"


def get_transactions(customer_id: str, limit: int = 5):
    """Retrieve recent transactions for a customer."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            t.transaction_id,
            t.merchant,
            t.amount,
            t.transaction_type,
            t.location,
            t.status,
            t.risk_score
        FROM transactions t
        JOIN accounts a
            ON t.account_id = a.account_id
        WHERE a.customer_id = ?
        ORDER BY t.rowid DESC
        LIMIT ?
        """,
        (customer_id, limit)
    )

    transactions = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {
        "success": True,
        "transactions": transactions
    }


def get_transaction(transaction_id: str):
    """Retrieve a specific transaction."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            t.transaction_id,
            t.account_id,
            t.merchant,
            t.amount,
            t.transaction_type,
            t.location,
            t.status,
            t.risk_score
        FROM transactions t
        WHERE t.transaction_id = ?
        """,
        (transaction_id,)
    )

    transaction = cursor.fetchone()
    conn.close()

    if not transaction:
        return {
            "success": False,
            "message": f"Transaction {transaction_id} not found."
        }

    return {
        "success": True,
        "transaction": dict(transaction)
    }