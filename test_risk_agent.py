from agents.risk_agent import risk_agent


queries = [
    "Is transaction TXN003 suspicious?",
    "Check transaction TXN001 for fraud",
    "Show my suspicious transactions"
]


for query in queries:

    print("\n" + "=" * 60)
    print("USER:", query)

    result = risk_agent(query)

    print("AGENT:", result["agent"])
    print("ACTION:", result["action"])
    print("RESULT:", result["result"])