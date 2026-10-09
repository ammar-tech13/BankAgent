from tools.credit_tools import (
    get_credit_score,
    get_existing_loans
)

from tools.loan_tools import (
    check_loan_eligibility,
    calculate_emi
)

import re


def credit_agent(query: str, customer_id: str = "CUST001"):
    """
    Credit/Loan Agent.

    Handles credit score, loans, loan eligibility
    and EMI calculations.
    """

    query_lower = query.lower()

    # Credit score
    if "credit score" in query_lower:
        result = get_credit_score(customer_id)

        return {
            "agent": "Credit/Loan Agent",
            "action": "get_credit_score",
            "result": result
        }

    # Existing loans
    if (
        "existing loan" in query_lower
        or "my loans" in query_lower
        or "current loan" in query_lower
    ):
        result = get_existing_loans(customer_id)

        return {
            "agent": "Credit/Loan Agent",
            "action": "get_existing_loans",
            "result": result
        }

    # Loan eligibility
    if (
        "eligible" in query_lower
        or "eligibility" in query_lower
    ):
        # Extract requested amount if provided
        numbers = re.findall(r"\d+(?:,\d+)*(?:\.\d+)?", query)

        requested_amount = 500000.0

        if numbers:
            requested_amount = float(numbers[0].replace(",", ""))

            # Handle lakh notation
            if "lakh" in query_lower:
                requested_amount *= 100000

        result = check_loan_eligibility(
            customer_id,
            requested_amount
        )

        return {
            "agent": "Credit/Loan Agent",
            "action": "check_loan_eligibility",
            "result": result
        }

    # EMI calculation
    if "emi" in query_lower:
        result = calculate_emi(
            principal=500000,
            annual_interest_rate=10.5,
            tenure_years=3
        )

        return {
            "agent": "Credit/Loan Agent",
            "action": "calculate_emi",
            "result": result
        }

    return {
        "agent": "Credit/Loan Agent",
        "action": "unknown",
        "result": {
            "success": False,
            "message": "I could not determine the requested credit operation."
        }
    }