import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="Oklahoma Home Affordability Estimator",
    page_icon="🏡",
    layout="wide"
)

# -----------------------------
# GOOGLE SHEETS CONNECTION
# -----------------------------
@st.cache_resource
def connect_to_google_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds_dict = dict(st.secrets["gcp_service_account"])

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict,
        scope
    )

    client = gspread.authorize(creds)
    sheet = client.open("Oklahoma Buyer Leads").sheet1
    return sheet


try:
    sheet = connect_to_google_sheet()
except Exception as e:
    sheet = None
    st.error(f"Google Sheets connection failed: {e}")


# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: #F5F7FB;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    h1, h2, h3 {
        color: #0B1F3A;
    }

    .hero {
        background: linear-gradient(135deg, #0B1F3A, #163D73);
        padding: 35px;
        border-radius: 24px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }

    .hero h1 {
        color: white;
        font-size: 42px;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 18px;
        line-height: 1.5;
    }

    .gold {
        color: #D4A857;
        font-weight: 700;
    }

    .card {
        background: white;
        padding: 28px;
        border-radius: 22px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        margin-bottom: 22px;
        border: 1px solid #E7EAF0;
    }

    .side-card {
        background: white;
        padding: 25px;
        border-radius: 22px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        margin-bottom: 18px;
        border-left: 6px solid #D4A857;
    }

    .mini-card {
        background: #EEF3FA;
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 15px;
        color: #0B1F3A;
    }

    .warning-box {
        background: #FFF7DF;
        border-left: 5px solid #D4A857;
        padding: 16px;
        border-radius: 14px;
        color: #5A4300;
        margin-bottom: 20px;
    }

    .result-box {
        background: linear-gradient(135deg, #0B1F3A, #163D73);
        padding: 28px;
        border-radius: 22px;
        color: white;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }

    .result-box h2,
    .result-box h3 {
        color: white;
    }

    .stButton > button {
        background: linear-gradient(90deg, #0B1F3A, #163D73);
        color: white;
        border-radius: 14px;
        height: 52px;
        width: 100%;
        font-size: 18px;
        border: none;
        font-weight: 700;
    }

    .stButton > button:hover {
        background: #D4A857;
        color: #0B1F3A;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        border-radius: 12px;
        border: 1px solid #CBD5E1;
    }

    div[data-testid="stSelectbox"] div {
        border-radius: 12px;
    }

    .footer {
        text-align: center;
        color: #64748B;
        font-size: 14px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# HERO SECTION
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>🏡 Can You Afford to Buy in <span class="gold">Oklahoma?</span></h1>
    <p>
        Get a simple AI-powered estimate of what home price range may fit your budget.
        Built by <strong>Brandi Kitchens</strong> — Oklahoma Realtor® + Python Developer + AI/LLM Engineer.
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# LAYOUT
# -----------------------------
left_col, right_col = st.columns([1, 2])


with left_col:
    st.markdown("""
    <div class="side-card">
        <h3>✨ Smarter Real Estate Decisions</h3>
        <p>This tool helps Oklahoma buyers understand what may be realistic before they start shopping.</p>
    </div>

    <div class="mini-card">
        <h4>📊 Know Your Numbers</h4>
        <p>Estimate a comfortable monthly payment and possible home price range.</p>
    </div>

    <div class="mini-card">
        <h4>🏡 Local Oklahoma Focus</h4>
        <p>Built for buyers looking in OKC, Norman, Moore, Edmond, Yukon, Mustang and surrounding areas.</p>
    </div>

    <div class="mini-card">
        <h4>🤖 Realtor + AI Advantage</h4>
        <p>Combining real estate experience, Python, automation, and AI-powered tools.</p>
    </div>

    <div class="mini-card">
        <h4>🔒 No Obligation</h4>
        <p>This is only an estimate. A licensed lender can give you exact approval numbers.</p>
    </div>
    """, unsafe_allow_html=True)


with right_col:
    st.markdown("""
    <div class="warning-box">
        ⚠️ This is an estimate only and not a loan approval. A licensed lender can give you exact numbers.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Step 1: Your Budget")

    col1, col2 = st.columns(2)

    with col1:
        monthly_income = st.number_input(
            "Estimated monthly household income before taxes",
            min_value=0,
            step=100
        )

        current_rent = st.number_input(
            "How much are you currently paying in rent?",
            min_value=0,
            step=50
        )

        credit_range = st.selectbox(
            "How would you describe your credit?",
            [
                "Select one",
                "Excellent: 740+",
                "Good: 680–739",
                "Fair: 620–679",
                "Needs work: under 620",
                "Not sure"
            ]
        )

    with col2:
        monthly_debts = st.number_input(
            "Estimated monthly debts — car payment, credit cards, loans, etc.",
            min_value=0,
            step=50
        )

        down_payment = st.number_input(
            "How much do you have saved for down payment/closing costs?",
            min_value=0,
            step=500
        )

        city = st.selectbox(
            "Where are you hoping to buy?",
            [
                "Oklahoma City",
                "Norman",
                "Moore",
                "Edmond",
                "Midwest City",
                "Yukon",
                "Mustang",
                "Newcastle",
                "Blanchard",
                "Other Oklahoma area"
            ]
        )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Step 2: Your Contact Info")

    contact_col1, contact_col2 = st.columns(2)

    with contact_col1:
        first_name = st.text_input("First name")
        email = st.text_input("Email")

    with contact_col2:
        last_name = st.text_input("Last name")
        phone = st.text_input("Phone number")

    st.markdown('</div>', unsafe_allow_html=True)

    submitted = st.button("✨ Get My Estimate")

    if submitted:
        if monthly_income == 0 or credit_range == "Select one" or not first_name or not email:
            st.error("Please complete your income, credit range, first name, and email.")
        else:
            max_housing_payment = monthly_income * 0.31
            estimated_payment_after_debts = max_housing_payment - (monthly_debts * 0.15)

            if estimated_payment_after_debts < 800:
                estimated_payment_after_debts = 800

            low_price = estimated_payment_after_debts * 120
            high_price = estimated_payment_after_debts * 145

            st.markdown(f"""
            <div class="result-box">
                <h2>{first_name}, here is your quick estimate:</h2>

                <h3>Estimated Comfortable Monthly Housing Payment</h3>
                <p style="font-size: 28px; font-weight: bold;">
                    ${estimated_payment_after_debts:,.0f} per month
                </p>

                <h3>Estimated Home Price Range</h3>
                <p style="font-size: 28px; font-weight: bold;">
                    ${low_price:,.0f} – ${high_price:,.0f}
                </p>
            </div>
            """, unsafe_allow_html=True)

            if credit_range in ["Excellent: 740+", "Good: 680–739"]:
                st.success("You may be in a strong position to start comparing loan options with a lender.")
            elif credit_range == "Fair: 620–679":
                st.info("You may still have options, especially with FHA or first-time buyer programs.")
            elif credit_range == "Needs work: under 620":
                st.warning("You may need a credit-readiness plan first, but that does not mean homeownership is impossible.")
            else:
                st.info("Your next best step is to have a lender review your full picture.")

            st.markdown("""
            ### Want help with the next step?
            I can help you create a buyer game plan, connect you with a lender, or help you understand what homes may fit your budget.
            """)

            lead = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "monthly_income": monthly_income,
                "monthly_debts": monthly_debts,
                "current_rent": current_rent,
                "down_payment": down_payment,
                "credit_range": credit_range,
                "city": city,
                "estimated_payment": round(estimated_payment_after_debts, 2),
                "estimated_low_price": round(low_price, 2),
                "estimated_high_price": round(high_price, 2)
            }

            try:
                if sheet is None:
                    raise Exception("Google Sheet is not connected.")

                sheet.append_row([
                    lead["timestamp"],
                    lead["first_name"],
                    lead["last_name"],
                    lead["email"],
                    lead["phone"],
                    lead["monthly_income"],
                    lead["monthly_debts"],
                    lead["current_rent"],
                    lead["down_payment"],
                    lead["credit_range"],
                    lead["city"],
                    lead["estimated_payment"],
                    lead["estimated_low_price"],
                    lead["estimated_high_price"]
                ])

                st.caption("✅ Your information has been saved for follow-up.")

            except Exception as e:
                st.error(f"Something went wrong saving the lead: {e}")


# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<div class="footer">
    Built by Brandi Kitchens | Oklahoma Realtor® | Python Developer | AI/LLM Engineer
</div>
""", unsafe_allow_html=True)