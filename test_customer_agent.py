from agents.customer_agent import customer_agent


queries = [
    "Show my account balance",
    "Show my recent transactions",
    "Show my customer profile",
    "Show transaction TXN003"
]


for query in queries:

    print("\n" + "=" * 60)
    print("USER:", query)

    result = customer_agent(query)

    print("AGENT:", result["agent"])
    print("ACTION:", result["action"])
    print("RESULT:", result["result"])