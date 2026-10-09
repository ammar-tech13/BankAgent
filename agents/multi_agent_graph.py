from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, START, END

from agents.supervisor import supervisor
from agents.customer_agent import customer_agent
from agents.risk_agent import risk_agent
from agents.credit_agent import credit_agent

from tools.transaction_tools import get_transactions
from tools.fraud_tools import analyze_transaction

from utils.response_formatter import format_response


class BankingState(TypedDict):
    user_query: str
    route: list[str]
    responses: Annotated[list[str], operator.add]
    response: str
    transactions: list
    workflow: Annotated[list[str], operator.add]


def supervisor_node(state):
    result = supervisor(state)

    return {
        "route": result["route"],
        "workflow": ["Supervisor"]
    }


def customer_node(state):
    result = customer_agent(state["user_query"])

    return {
        "responses": [format_response(result)],
        "workflow": ["Customer Agent"]
    }


def risk_node(state):
    result = risk_agent(state["user_query"])

    return {
        "responses": [format_response(result)],
        "workflow": ["Risk Agent"]
    }


def credit_node(state):
    result = credit_agent(state["user_query"])

    return {
        "responses": [format_response(result)],
        "workflow": ["Credit/Loan Agent"]
    }


def recent_transaction_workflow(state):
    """
    Multi-step agentic workflow:
    1. Fetch recent transactions
    2. Analyze each transaction for fraud risk
    3. Report highly suspicious transactions
    """

    customer_id = "CUST001"

    # Step 1: Get recent transactions
    transactions_result = get_transactions(
        customer_id,
        limit=5
    )

    workflow_steps = [
        "Customer Agent",
        "Transaction Tool"
    ]

    if not transactions_result.get("success"):
        return {
            "responses": [
                "Unable to retrieve recent transactions."
            ],
            "workflow": workflow_steps
        }

    transactions = transactions_result.get(
        "transactions",
        []
    )

    suspicious_results = []

    # Step 2: Risk analysis
    for transaction in transactions:

        transaction_id = transaction.get(
            "transaction_id"
        )

        if not transaction_id:
            continue

        risk_result = analyze_transaction(
            transaction_id
        )

        if not risk_result.get("success"):
            continue

        if risk_result.get("risk_level") == "HIGH":
            suspicious_results.append(
                risk_result
            )

    workflow_steps.extend([
        "Risk Agent",
        "Fraud Analysis Tool"
    ])

    # Step 3: Final decision
    if suspicious_results:

        response = (
            "🚨 Suspicious Activity Detected\n\n"
        )

        for result in suspicious_results:

            transaction = result.get(
                "transaction",
                {}
            )

            response += (
                f"Transaction: "
                f"{transaction.get('transaction_id', 'N/A')}\n"
                f"Merchant: "
                f"{transaction.get('merchant', 'N/A')}\n"
                f"Amount: "
                f"₹{transaction.get('amount', 0):,.2f}\n"
                f"Location: "
                f"{transaction.get('location', 'N/A')}\n"
                f"Risk Score: "
                f"{result.get('risk_score', 0) * 100:.0f}%\n"
                f"Risk Level: "
                f"{result.get('risk_level', 'UNKNOWN')}\n"
                f"Recommendation: "
                f"{result.get('recommendation', 'Review required.')}\n\n"
            )

    else:

        response = (
            "✅ No highly suspicious transactions "
            "were detected in your recent transactions."
        )

    return {
        "responses": [response],
        "workflow": workflow_steps
    }

def final_response_node(state):

    combined_response = "\n\n".join(state["responses"])

    return {
        "response": combined_response
    }


def route_to_agents(state):

    query = state["user_query"].lower()

    # Special multi-step workflow
    if (
        ("recent" in query or "transactions" in query)
        and (
            "suspicious" in query
            or "fraud" in query
            or "risky" in query
        )
    ):
        return "transaction_risk_workflow"

    routes = state["route"]

    return routes


graph = StateGraph(BankingState)

graph.add_node("supervisor", supervisor_node)

graph.add_node("customer", customer_node)
graph.add_node("risk", risk_node)
graph.add_node("credit", credit_node)

graph.add_node(
    "transaction_risk_workflow",
    recent_transaction_workflow
)

graph.add_node("final_response", final_response_node)


graph.add_edge(START, "supervisor")


graph.add_conditional_edges(
    "supervisor",
    route_to_agents,
    {
        "transaction_risk_workflow": "transaction_risk_workflow",
        "customer": "customer",
        "risk": "risk",
        "credit": "credit"
    }
)


graph.add_edge(
    "transaction_risk_workflow",
    "final_response"
)

graph.add_edge("customer", "final_response")
graph.add_edge("risk", "final_response")
graph.add_edge("credit", "final_response")

graph.add_edge("final_response", END)


banking_graph = graph.compile()