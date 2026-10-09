import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

load_dotenv()


class BankingState(TypedDict):
    user_query: str
    route: list[str]
    response: str


llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0
)


def extract_text(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, str):
                text_parts.append(item)

            elif isinstance(item, dict):
                if "text" in item:
                    text_parts.append(str(item["text"]))

        return " ".join(text_parts)

    return str(content)


def supervisor(state: BankingState):
    query = state["user_query"].lower()

    routes = []

    risk_keywords = [
        "fraud",
        "suspicious",
        "risk",
        "risky",
        "scam",
        "fraud detection"
    ]

    credit_keywords = [
        "credit score",
        "credit",
        "loan",
        "eligible",
        "eligibility",
        "emi",
        "loan calculation",
        "existing loan",
        "my loans"
    ]

    customer_keywords = [
        "balance",
        "account",
        "profile",
        "personal details",
        "recent transactions"
    ]

    # Risk/Fraud has priority when fraud-related intent is detected
    if any(keyword in query for keyword in risk_keywords):
        routes.append("risk")

    # Credit/Loan routing
    if any(keyword in query for keyword in credit_keywords):
        routes.append("credit")

    # Customer banking routing
    # Don't route transaction-related fraud queries to customer agent
    if any(keyword in query for keyword in customer_keywords):
        routes.append("customer")

    routes = list(dict.fromkeys(routes))

    if not routes:
        routes = ["customer"]

    return {"route": routes}

def build_supervisor_graph():

    graph = StateGraph(BankingState)

    graph.add_node("supervisor", supervisor)

    graph.add_edge(START, "supervisor")
    graph.add_edge("supervisor", END)

    return graph.compile()


supervisor_graph = build_supervisor_graph()