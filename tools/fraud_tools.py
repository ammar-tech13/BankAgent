import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "banking.db"


def analyze_transaction(transaction_id: str):
    """
    Analyze a transaction and classify its fraud risk.
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            transaction_id,
            merchant,
            amount,
            location,
            status,
            risk_score
        FROM transactions
        WHERE transaction_id = ?
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

    transaction = dict(transaction)

    risk_score = transaction["risk_score"]

    if risk_score >= 0.80:
        risk_level = "HIGH"
        recommendation = "Transaction should be reviewed immediately."
    elif risk_score >= 0.50:
        risk_level = "MEDIUM"
        recommendation = "Additional verification is recommended."
    else:
        risk_level = "LOW"
        recommendation = "Transaction appears normal."

    return {
        "success": True,
        "transaction_id": transaction_id,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "transaction": transaction
    }


def get_suspicious_transactions(customer_id: str):
    """
    Retrieve transactions with high fraud risk.
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            t.transaction_id,
            t.merchant,
            t.amount,
            t.location,
            t.status,
            t.risk_score
        FROM transactions t
        JOIN accounts a
            ON t.account_id = a.account_id
        WHERE a.customer_id = ?
        AND t.risk_score >= 0.50
        ORDER BY t.risk_score DESC
        """,
        (customer_id,)
    )

    transactions = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {
        "success": True,
        "count": len(transactions),
        "transactions": transactions
    }