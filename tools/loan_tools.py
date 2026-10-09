import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "banking.db"


def check_loan_eligibility(
    customer_id: str,
    requested_amount: float
):
    """
    Perform a simulated personal-loan eligibility check.

    Demo policy:
    - Minimum credit score: 700
    - Minimum monthly income: ₹30,000
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    # Get customer income
    cursor.execute(
        """
        SELECT monthly_income
        FROM customers
        WHERE customer_id = ?
        """,
        (customer_id,)
    )

    customer = cursor.fetchone()

    # Get credit score
    cursor.execute(
        """
        SELECT credit_score
        FROM credit
        WHERE customer_id = ?
        """,
        (customer_id,)
    )

    credit = cursor.fetchone()

    # Get existing EMI
    cursor.execute(
        """
        SELECT COALESCE(SUM(monthly_emi), 0)
        FROM loans
        WHERE customer_id = ?
        AND status = 'Active'
        """,
        (customer_id,)
    )

    existing_emi = cursor.fetchone()[0]

    conn.close()

    if not customer:
        return {
            "success": False,
            "message": f"Customer {customer_id} not found."
        }

    if not credit:
        return {
            "success": False,
            "message": f"Credit information for {customer_id} not found."
        }

    monthly_income = customer["monthly_income"]
    credit_score = credit["credit_score"]

    debt_ratio = existing_emi / monthly_income

    credit_requirement = credit_score >= 700
    income_requirement = monthly_income >= 30000
    debt_requirement = debt_ratio <= 0.40

    eligible = (
        credit_requirement
        and income_requirement
        and debt_requirement
    )

    reasons = []

    if not credit_requirement:
        reasons.append("Credit score is below 700.")

    if not income_requirement:
        reasons.append("Monthly income is below ₹30,000.")

    if not debt_requirement:
        reasons.append("Existing EMI burden exceeds 40% of income.")

    if eligible:
        decision = "ELIGIBLE"
        reasons.append(
            "Customer satisfies the simulated credit, income and debt-ratio criteria."
        )
    else:
        decision = "NOT ELIGIBLE"

    return {
        "success": True,
        "customer_id": customer_id,
        "requested_amount": requested_amount,
        "monthly_income": monthly_income,
        "credit_score": credit_score,
        "existing_emi": existing_emi,
        "debt_ratio": round(debt_ratio, 3),
        "decision": decision,
        "reasons": reasons
    }


def calculate_emi(
    principal: float,
    annual_interest_rate: float,
    tenure_years: int
):
    """
    Calculate monthly EMI using the standard reducing-balance formula.
    """

    if principal <= 0:
        return {
            "success": False,
            "message": "Principal must be greater than zero."
        }

    if annual_interest_rate < 0:
        return {
            "success": False,
            "message": "Interest rate cannot be negative."
        }

    if tenure_years <= 0:
        return {
            "success": False,
            "message": "Tenure must be greater than zero."
        }

    monthly_rate = annual_interest_rate / 12 / 100
    months = tenure_years * 12

    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** months
            / ((1 + monthly_rate) ** months - 1)
        )

    total_payment = emi * months
    total_interest = total_payment - principal

    return {
        "success": True,
        "principal": principal,
        "annual_interest_rate": annual_interest_rate,
        "tenure_years": tenure_years,
        "monthly_emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2)
    }