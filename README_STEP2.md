# BankAgent — Step 2: Simulated Banking Database

This step creates a realistic local SQLite banking database seeded from JSON data.

## Data included
- Customers
- Accounts
- Transactions
- Loans
- Credit scores

## Setup

From the BankAgent project root:

```bash
python database/banking_db.py
```

Expected output:

```text
Banking database initialized: .../banking.db
```

The database is intentionally simulated. It contains no real customer information.

## Demo customer

Use `CUST001` for the main demo:

- Rahul Sharma
- Savings balance: ₹82,450
- Credit score: 742
- Existing EMI: ₹8,000
- Transaction `TXN003`: ₹85,000, flagged as high risk
