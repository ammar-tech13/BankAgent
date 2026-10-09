from agents.multi_agent_graph import banking_graph


queries = [
    "Show my account balance",
    "Is transaction TXN003 suspicious?",
    "What is my credit score?",
    "Am I eligible for a 5 lakh personal loan?",
    "Show my balance and check if I am eligible for a 5 lakh personal loan",
    "Show my balance and tell me if there are any suspicious transactions",
    "Check my recent transactions for suspicious activity"
]


for query in queries:

    print("\n" + "=" * 70)
    print("USER:")
    print(query)

    result = banking_graph.invoke({
        "user_query": query,
        "route": [],
        "responses": [],
        "response": "",
        "transactions": [],
    "workflow": []
    })

    print("\nROUTED TO:")
    print(result["route"])

    print("\nAGENT RESPONSE:")
    print(result["response"])