from agents.supervisor import supervisor_graph


queries = [
    "Show my account balance",
    "Is transaction TXN003 suspicious?",
    "Am I eligible for a 5 lakh personal loan?",
    "What is my credit score?",
    "Show my recent transactions"
]


for query in queries:

    result = supervisor_graph.invoke({
        "user_query": query,
        "route": "",
        "response": ""
    })

    print("\nUSER:", query)
    print("ROUTE:", result["route"])