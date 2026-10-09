import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "banking.db"


def get_credit_score(customer_id: str):
    """Retrieve customer's credit score."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT customer_id, credit_score
        FROM credit
        WHERE customer_id = ?
        """,
        (customer_id,)
    )

    credit = cursor.fetchone()
    conn.close()

    if not credit:
        return {
            "success": False,
            "message": f"Credit information for {customer_id} not found."
        }

    return {
        "success": True,
        "credit": dict(credit)
    }


def get_existing_loans(customer_id: str):
    """Retrieve active loans for a customer."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            loan_id,
            loan_type,
            principal,
            outstanding,
            monthly_emi,
            status
        FROM loans
        WHERE customer_id = ?
        AND status = 'Active'
        """,
        (customer_id,)
    )

    loans = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {
        "success": True,
        "loans": loans
    }