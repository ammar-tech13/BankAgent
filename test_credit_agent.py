from agents.credit_agent import credit_agent


queries = [
    "What is my credit score?",
    "Show my existing loans",
    "Am I eligible for a 5 lakh personal loan?",
    "Calculate EMI for my loan"
]


for query in queries:

    print("\n" + "=" * 60)
    print("USER:", query)

    result = credit_agent(query)

    print("AGENT:", result["agent"])
    print("ACTION:", result["action"])
    print("RESULT:", result["result"])