from tools.customer_tools import (
    get_customer_profile,
    get_account_balance
)

from tools.transaction_tools import (
    get_transactions,
    get_transaction
)


def customer_agent(query: str, customer_id: str = "CUST001"):
    """
    Customer Banking Agent.

    Handles account, profile and transaction-related requests.
    """

    query_lower = query.lower()

    # Account balance
    if "balance" in query_lower:
        result = get_account_balance(customer_id)

        return {
            "agent": "Customer Banking Agent",
            "action": "get_account_balance",
            "result": result
        }

    # Customer profile
    if "profile" in query_lower or "personal details" in query_lower:
        result = get_customer_profile(customer_id)

        return {
            "agent": "Customer Banking Agent",
            "action": "get_customer_profile",
            "result": result
        }

    # Specific transaction
    if "transaction" in query_lower and "txn" in query_lower:
        import re

        match = re.search(r"TXN\d+", query.upper())

        if match:
            transaction_id = match.group()

            result = get_transaction(transaction_id)

            return {
                "agent": "Customer Banking Agent",
                "action": "get_transaction",
                "result": result
            }

    # Recent transactions
    if (
        "transaction" in query_lower
        or "transactions" in query_lower
        or "recent" in query_lower
    ):
        result = get_transactions(customer_id)

        return {
            "agent": "Customer Banking Agent",
            "action": "get_transactions",
            "result": result
        }

    return {
        "agent": "Customer Banking Agent",
        "action": "unknown",
        "result": {
            "success": False,
            "message": "I could not determine the requested banking operation."
        }
    }