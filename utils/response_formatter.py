def format_response(agent_result):
    agent = agent_result.get("agent", "")
    action = agent_result.get("action", "")
    result = agent_result.get("result", {})

    if not result.get("success", False):
        return f"❌ {result.get('message', 'Unable to process the request.')}"

    # Customer Banking Agent
    if agent == "Customer Banking Agent":

        if action == "get_account_balance":
            accounts = result.get("accounts", [])

            if not accounts:
                return "No active bank accounts were found."

            lines = ["🏦 Account Information", ""]

            for account in accounts:
                lines.append(
                    f"Account: {account['account_id']}\n"
                    f"Type: {account['type']}\n"
                    f"Balance: ₹{account['balance']:,.2f}\n"
                    f"Status: {account['status']}"
                )

            return "\n\n".join(lines)

        if action == "get_customer_profile":
            customer = result.get("customer", {})

            return (
                "👤 Customer Profile\n\n"
                f"Customer ID: {customer.get('customer_id')}\n"
                f"Name: {customer.get('name')}\n"
                f"Age: {customer.get('age')}\n"
                f"City: {customer.get('city')}\n"
                f"Occupation: {customer.get('occupation')}\n"
                f"Monthly Income: ₹{customer.get('monthly_income', 0):,.2f}"
            )

        if action == "get_transactions":
            transactions = result.get("transactions", [])

            if not transactions:
                return "No recent transactions found."

            lines = ["💳 Recent Transactions", ""]

            for tx in transactions:
                lines.append(
                    f"{tx['transaction_id']} | "
                    f"{tx['merchant']} | "
                    f"₹{tx['amount']:,.2f} | "
                    f"{tx['location']} | "
                    f"{tx['status']}"
                )

            return "\n".join(lines)

        if action == "get_transaction":
            tx = result.get("transaction", {})

            return (
                "💳 Transaction Details\n\n"
                f"Transaction: {tx.get('transaction_id')}\n"
                f"Merchant: {tx.get('merchant')}\n"
                f"Amount: ₹{tx.get('amount', 0):,.2f}\n"
                f"Location: {tx.get('location')}\n"
                f"Status: {tx.get('status')}\n"
                f"Risk Score: {tx.get('risk_score', 0) * 100:.0f}%"
            )

    # Risk / Fraud Agent
    if agent == "Risk/Fraud Agent":

        if action == "analyze_transaction":
            tx = result.get("transaction", {})

            risk_level = result.get("risk_level", "UNKNOWN")
            risk_score = result.get("risk_score", 0) * 100

            return (
                f"🚨 Transaction Risk Analysis\n\n"
                f"Transaction: {result.get('transaction_id')}\n"
                f"Merchant: {tx.get('merchant')}\n"
                f"Amount: ₹{tx.get('amount', 0):,.2f}\n"
                f"Location: {tx.get('location')}\n"
                f"Status: {tx.get('status')}\n"
                f"Risk Score: {risk_score:.0f}%\n"
                f"Risk Level: {risk_level}\n\n"
                f"Recommendation: {result.get('recommendation')}"
            )

        if action == "get_suspicious_transactions":
            transactions = result.get("transactions", [])

            if not transactions:
                return "✅ No suspicious transactions were detected."

            lines = [
                f"⚠️ Suspicious Transactions Detected: {len(transactions)}",
                ""
            ]

            for tx in transactions:
                lines.append(
                    f"{tx['transaction_id']} | "
                    f"{tx['merchant']} | "
                    f"₹{tx['amount']:,.2f} | "
                    f"Risk: {tx['risk_score'] * 100:.0f}%"
                )

            return "\n".join(lines)

    # Credit / Loan Agent
    if agent == "Credit/Loan Agent":

        if action == "get_credit_score":
            credit = result.get("credit", {})

            return (
                "📊 Credit Information\n\n"
                f"Customer ID: {credit.get('customer_id')}\n"
                f"Credit Score: {credit.get('credit_score')}"
            )

        if action == "get_existing_loans":
            loans = result.get("loans", [])

            if not loans:
                return "You currently have no active loans."

            lines = ["💰 Existing Loans", ""]

            for loan in loans:
                lines.append(
                    f"{loan['loan_id']} | {loan['loan_type']}\n"
                    f"Principal: ₹{loan['principal']:,.2f}\n"
                    f"Outstanding: ₹{loan['outstanding']:,.2f}\n"
                    f"Monthly EMI: ₹{loan['monthly_emi']:,.2f}\n"
                    f"Status: {loan['status']}"
                )

            return "\n\n".join(lines)

        if action == "check_loan_eligibility":
            decision = result.get("decision")

            if decision == "ELIGIBLE":
                status = "✅ ELIGIBLE"
            else:
                status = "❌ NOT ELIGIBLE"

            reasons = "\n".join(
                f"• {reason}" for reason in result.get("reasons", [])
            )

            return (
                f"🏦 Loan Eligibility\n\n"
                f"Requested Amount: ₹{result.get('requested_amount', 0):,.2f}\n"
                f"Credit Score: {result.get('credit_score')}\n"
                f"Monthly Income: ₹{result.get('monthly_income', 0):,.2f}\n"
                f"Existing EMI: ₹{result.get('existing_emi', 0):,.2f}\n"
                f"Debt Ratio: {result.get('debt_ratio', 0) * 100:.1f}%\n\n"
                f"Decision: {status}\n\n"
                f"Reason:\n{reasons}"
            )

        if action == "calculate_emi":
            return (
                "🧮 EMI Calculation\n\n"
                f"Loan Amount: ₹{result.get('principal', 0):,.2f}\n"
                f"Interest Rate: {result.get('annual_interest_rate')}% per year\n"
                f"Tenure: {result.get('tenure_years')} years\n\n"
                f"Monthly EMI: ₹{result.get('monthly_emi', 0):,.2f}\n"
                f"Total Payment: ₹{result.get('total_payment', 0):,.2f}\n"
                f"Total Interest: ₹{result.get('total_interest', 0):,.2f}"
            )

    return "The request was processed successfully."