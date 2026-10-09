from tools.fraud_tools import (
    analyze_transaction,
    get_suspicious_transactions
)

from tools.loan_tools import (
    check_loan_eligibility,
    calculate_emi
)


from tools.customer_tools import (
    get_customer_profile,
    get_account_balance
)

from tools.transaction_tools import (
    get_transactions,
    get_transaction
)

from tools.credit_tools import (
    get_credit_score,
    get_existing_loans
)


customer_id = "CUST001"


print("\n========== CUSTOMER ==========")
print(get_customer_profile(customer_id))

print("\n========== ACCOUNT ==========")
print(get_account_balance(customer_id))

print("\n========== TRANSACTIONS ==========")
print(get_transactions(customer_id))

print("\n========== SINGLE TRANSACTION ==========")
print(get_transaction("TXN003"))

print("\n========== CREDIT ==========")
print(get_credit_score(customer_id))

print("\n========== LOANS ==========")
print(get_existing_loans(customer_id))
print("\n========== FRAUD ANALYSIS ==========")
print(analyze_transaction("TXN003"))

print("\n========== SUSPICIOUS TRANSACTIONS ==========")
print(get_suspicious_transactions("CUST001"))

print("\n========== LOAN ELIGIBILITY ==========")
print(check_loan_eligibility("CUST001", 500000))

print("\n========== EMI CALCULATION ==========")
print(calculate_emi(500000, 10.5, 3))