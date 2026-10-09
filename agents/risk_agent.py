from tools.fraud_tools import (
    analyze_transaction,
    get_suspicious_transactions
)


def risk_agent(query: str, customer_id: str = "CUST001"):
    """
    Risk/Fraud Agent.

    Handles fraud detection, transaction risk analysis,
    and suspicious transaction identification.
    """

    query_lower = query.lower()

    # Analyze a specific transaction
    if "txn" in query_lower or "transaction" in query_lower:

        import re

        match = re.search(r"TXN\d+", query.upper())

        if match:
            transaction_id = match.group()

            result = analyze_transaction(transaction_id)

            return {
                "agent": "Risk/Fraud Agent",
                "action": "analyze_transaction",
                "result": result
            }

    # Find suspicious transactions
    if (
        "suspicious" in query_lower
        or "fraud" in query_lower
        or "risky" in query_lower
    ):
        result = get_suspicious_transactions(customer_id)

        return {
            "agent": "Risk/Fraud Agent",
            "action": "get_suspicious_transactions",
            "result": result
        }

    return {
        "agent": "Risk/Fraud Agent",
        "action": "unknown",
        "result": {
            "success": False,
            "message": "I could not determine the requested risk operation."
        }
    }