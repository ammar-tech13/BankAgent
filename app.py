
import re
import streamlit as st

from agents.multi_agent_graph import banking_graph
from tools.customer_tools import get_account_balance
from tools.credit_tools import get_credit_score


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="BankAgent AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# PREMIUM DARK UI
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #0b1120;
        color: #e2e8f0;
    }

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #263244;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    div[data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #263244;
        padding: 18px;
        border-radius: 12px;
    }

    div.stButton > button {
        border-radius: 9px;
        min-height: 42px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

for key, default in {
    "result": None,
    "last_query": "",
    "query_input": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

CUSTOMER_ID = "CUST001"


# =========================================================
# ROBUST TOOL VALUE EXTRACTION
# =========================================================

def extract_number(value, patterns):
    """Extract a numeric value from text using possible labels."""
    if value is None:
        return None

    text = str(value)

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1).replace(",", "").replace("₹", "").strip())
            except (ValueError, AttributeError):
                continue

    return None


def find_dict_value(data, keys):
    """Search nested dictionaries for a matching field."""
    if not isinstance(data, dict):
        return None

    for key in keys:
        if key in data and data[key] is not None:
            return data[key]

    for value in data.values():
        found = find_dict_value(value, keys)
        if found is not None:
            return found

    return None


def get_live_balance():
    """Read the real balance through the existing account tool."""
    try:
        data = get_account_balance(CUSTOMER_ID)

        if isinstance(data, (int, float)):
            return float(data)

        value = find_dict_value(
            data,
            [
                "balance",
                "available_balance",
                "account_balance",
                "current_balance",
            ],
        )

        if value is not None:
            try:
                return float(
                    str(value).replace(",", "").replace("₹", "").strip()
                )
            except ValueError:
                pass

        # Handle a formatted string or dictionary containing account details.
        text = str(data)

        return extract_number(
            text,
            [
                r"(?:available\s+)?balance\s*['\"]?\s*:\s*['\"]?\s*₹?\s*([\d,]+(?:\.\d+)?)",
                r"['\"]balance['\"]\s*:\s*['\"]?₹?\s*([\d,]+(?:\.\d+)?)",
            ],
        )

    except Exception as error:
        st.sidebar.warning(f"Account tool error: {error}")
        return None


def get_live_credit_score():
    """Read the credit score through the existing credit tool."""
    try:
        data = get_credit_score(CUSTOMER_ID)

        if isinstance(data, (int, float)):
            return int(data)

        value = find_dict_value(
            data,
            ["credit_score", "score"],
        )

        if value is not None:
            try:
                return int(float(value))
            except (ValueError, TypeError):
                pass

        return extract_number(
            str(data),
            [
                r"credit\s+score\s*:\s*(\d{3})",
                r"score\s*:\s*(\d{3})",
            ],
        )

    except Exception:
        return None


# =========================================================
# RUN THE EXISTING MULTI-AGENT GRAPH
# =========================================================

def run_query(query):
    query = query.strip()

    if not query:
        st.warning("Please enter a question or loan amount.")
        return

    try:
        with st.spinner("🧠 Supervisor is coordinating the agents..."):
            result = banking_graph.invoke(
                {
                    "user_query": query,
                    "route": [],
                    "responses": [],
                    "response": "",
                    "transactions": [],
                    "workflow": [],
                }
            )

        st.session_state.result = result
        st.session_state.last_query = query

    except Exception as error:
        st.error(f"BankAgent AI encountered an error: {error}")


# =========================================================
# LOAN RESPONSE FORMATTING
# =========================================================

def extract_label(response, label, following_labels):
    """Extract a labelled field from compact or multiline responses."""
    next_labels = "|".join(
        re.escape(item) for item in following_labels
    )

    pattern = (
        rf"{re.escape(label)}\s*:?\s*"
        rf"(.*?)"
        rf"(?=\s+(?:{next_labels})\s*:|$)"
    )

    match = re.search(pattern, response, re.IGNORECASE)

    if not match:
        return ""

    return match.group(1).strip(" \t\n:•")


def display_loan_response(response):
    st.subheader("💳 Loan Eligibility Analysis")

    amount = extract_label(
        response,
        "Requested Amount",
        ["Credit Score", "Monthly Income", "Existing EMI",
         "Debt Ratio", "Decision", "Reason"],
    )

    score = extract_label(
        response,
        "Credit Score",
        ["Monthly Income", "Existing EMI", "Debt Ratio",
         "Decision", "Reason"],
    )

    income = extract_label(
        response,
        "Monthly Income",
        ["Existing EMI", "Debt Ratio", "Decision", "Reason"],
    )

    emi = extract_label(
        response,
        "Existing EMI",
        ["Debt Ratio", "Decision", "Reason"],
    )

    ratio = extract_label(
        response,
        "Debt Ratio",
        ["Decision", "Reason"],
    )

    reason_match = re.search(
        r"Reason\s*:\s*(.*)",
        response,
        re.IGNORECASE,
    )
    reason = reason_match.group(1).strip() if reason_match else ""

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("💰 Requested Amount", amount or "Not provided")

    with c2:
        st.metric("📊 Credit Score", score or "—")

    with c3:
        st.metric("💵 Monthly Income", income or "—")

    c4, c5 = st.columns(2)

    with c4:
        st.metric("📉 Existing EMI", emi or "—")

    with c5:
        st.metric("📊 Debt Ratio", ratio or "—")

    # Test NOT ELIGIBLE before ELIGIBLE.
    if re.search(r"\bNOT\s+ELIGIBLE\b", response, re.IGNORECASE):
        st.error("❌ LOAN NOT ELIGIBLE")
    elif re.search(r"\bELIGIBLE\b", response, re.IGNORECASE):
        st.success("✅ LOAN ELIGIBLE")
    else:
        st.info("See the full response for the agent's decision.")

    if reason:
        st.info(f"📋 Reason: {reason}")

    with st.expander("View full agent response"):
        st.write(response)


def display_result():
    result = st.session_state.result

    if not result:
        return

    response = str(result.get("response", "") or "")
    workflow = result.get("workflow", [])

    st.divider()
    st.subheader("⚡ Agent Execution Trace")

    if workflow:
        for step in workflow:
            st.write(f"✅ {step}")
    else:
        st.caption("No execution trace was returned.")

    st.subheader("✨ AI Response")

    if (
        re.search(r"Requested Amount\s*:", response, re.IGNORECASE)
        or "Loan Eligibility" in response
    ):
        display_loan_response(response)

    elif (
        "suspicious" in response.lower()
        or "fraud" in response.lower()
        or "risk_score" in response.lower()
        or "risk level" in response.lower()
    ):
        st.warning(response)

    else:
        st.success(response)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("🏦 BankAgent AI")
    st.caption("Multi-Agent Banking Intelligence")

    st.success("● All systems operational")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Accounts",
            "Risk & Fraud",
            "Loans & Credit",
        ],
    )

    st.divider()
    st.subheader("🤖 AI AGENTS")
    st.write("🏦 Customer Agent")
    st.write("🛡️ Risk / Fraud Agent")
    st.write("💳 Credit / Loan Agent")
    st.write("🧠 Supervisor Agent")


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    left, right = st.columns([5, 1])

    with left:
        st.title("🏦 BankAgent AI")
        st.caption("Intelligent Multi-Agent Banking Assistant")

    with right:
        st.success("● AI System Online")

    st.header("Welcome back, Ammar 👋")
    st.caption(
        "Your intelligent banking assistant powered by "
        "multi-agent AI orchestration."
    )

    # Fetch values from the existing tools on each rerun.
    balance = get_live_balance()
    credit_score = get_live_credit_score()

    st.subheader("Account Overview")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "💰 Available Balance",
            f"₹{balance:,.2f}" if balance is not None else "Could not load",
        )

    with c2:
        st.metric(
            "📊 Credit Score",
            str(credit_score) if credit_score is not None else "Could not load",
        )

    with c3:
        st.metric("🛡️ Risk Status", "Monitoring Active")

    st.subheader("⚡ Quick Actions")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        if st.button("💰 Check Balance", use_container_width=True):
            st.session_state.query_input = "Show my account balance"
            run_query(st.session_state.query_input)

    with q2:
        if st.button("🛡️ Check Fraud", use_container_width=True):
            st.session_state.query_input = (
                "Check my recent transactions for suspicious activity"
            )
            run_query(st.session_state.query_input)

    with q3:
        if st.button("💳 Loan Eligibility", use_container_width=True):
            st.session_state.query_input = (
                "Am I eligible for a personal loan of ₹500000?"
            )
            run_query(st.session_state.query_input)

    with q4:
        if st.button("📊 Credit Score", use_container_width=True):
            st.session_state.query_input = "What is my credit score?"
            run_query(st.session_state.query_input)

    # Editable loan amount
    st.subheader("💳 Loan Eligibility Calculator")

    with st.form("loan_calculator_form"):
        loan_amount = st.number_input(
            "Enter requested loan amount (₹)",
            min_value=10000,
            max_value=10000000,
            value=500000,
            step=10000,
            format="%d",
            help="Choose any amount from ₹10,000 to ₹1,00,00,000.",
        )

        st.caption(f"Selected amount: ₹{loan_amount:,.0f}")

        check_loan = st.form_submit_button(
            "🔍 Check This Loan Amount",
            type="primary",
            use_container_width=True,
        )

    if check_loan:
        loan_query = (
            f"Am I eligible for a personal loan of ₹{loan_amount:.0f}?"
        )
        st.session_state.query_input = loan_query
        run_query(loan_query)

    st.divider()
    st.subheader("🤖 AI Banking Assistant")

    st.info(
        "✨ BankAgent AI\n\n"
        "Customer • Risk • Credit agents ready"
    )

    with st.form("ask_banking_assistant"):
        question = st.text_input(
            "Ask BankAgent AI",
            placeholder=(
                "Example: Is transaction TXN003 suspicious?"
            ),
        )

        ask = st.form_submit_button(
            "🚀 Ask BankAgent AI",
            use_container_width=True,
        )

    if ask:
        if question.strip():
            st.session_state.query_input = question.strip()
            run_query(question.strip())
        else:
            st.warning("Enter a question first.")

    display_result()


# =========================================================
# ACCOUNTS
# =========================================================

elif page == "Accounts":
    st.title("💰 Accounts")

    balance = get_live_balance()

    if balance is None:
        st.error(
            "The account tool did not return a readable balance. "
            "Check its actual return value."
        )
    else:
        st.metric("Available Balance", f"₹{balance:,.2f}")

    if st.button("Refresh Account Balance"):
        st.rerun()

    st.caption("Balance is read using the existing customer account tool.")


# =========================================================
# RISK & FRAUD
# =========================================================

elif page == "Risk & Fraud":
    st.title("🛡️ Risk & Fraud")

    st.write(
        "Analyze transactions using the existing Risk/Fraud Agent."
    )

    transaction_id = st.text_input(
        "Transaction ID",
        value="TXN003",
        key="risk_transaction_id",
    )

    if st.button("🔍 Analyze Transaction", type="primary"):
        run_query(
            f"Is transaction {transaction_id.strip()} suspicious?"
        )

    display_result()


# =========================================================
# LOANS & CREDIT
# =========================================================

elif page == "Loans & Credit":
    st.title("💳 Loans & Credit")

    score = get_live_credit_score()

    st.metric(
        "Credit Score",
        str(score) if score is not None else "Could not load",
    )

    with st.form("loans_page_form"):
        amount = st.number_input(
            "Requested loan amount (₹)",
            min_value=10000,
            max_value=10000000,
            value=500000,
            step=10000,
            format="%d",
        )

        submit_loan = st.form_submit_button(
            "Check Loan Eligibility",
            type="primary",
            use_container_width=True,
        )

    if submit_loan:
        run_query(
            f"Am I eligible for a personal loan of ₹{amount:.0f}?"
        )

    display_result()


# =========================================================
# FOOTER
# =========================================================

st.divider()
st.caption("BankAgent AI • Multi-Agent Banking Intelligence")
st.caption("Powered by LangGraph • LangChain • Python • SQLite")