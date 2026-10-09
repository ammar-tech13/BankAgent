from utils.response_formatter import format_response

from agents.customer_agent import customer_agent
from agents.risk_agent import risk_agent
from agents.credit_agent import credit_agent


tests = [
    customer_agent("Show my account balance"),
    risk_agent("Is transaction TXN003 suspicious?"),
    credit_agent("Am I eligible for a 5 lakh personal loan?")
]


for result in tests:
    print("\n" + "=" * 60)
    print(format_response(result))