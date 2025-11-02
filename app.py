import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import time

# Page configuration
st.set_page_config(
    page_title="Luxury Retail Financial Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 🔑 API CONFIGURATION - ONLY EDIT LINE 21
# ==============================================================================
# Get FREE API key: https://www.alphavantage.co/support/#api-key
# Free tier: 25 API calls per day (perfect for 5 companies)
ALPHA_VANTAGE_API_KEY = "YOUR_API_KEY_HERE"  # ← LINE 21: Replace with your actual key

# ==============================================================================
# COMPANY CONFIGURATIONS
# ==============================================================================
COMPANIES = {
    "LVMH": {
        "name": "LVMH Moët Hennessy Louis Vuitton",
        "ticker": "MC.PA",
        "exchange": "Euronext Paris",
        "currency": "EUR",
        "manual": {
            "Revenue": 86153000000,  # EUR 86.2B (FY2024)
            "EBITDA": 24463000000,
            "PBT": 21033000000,
            "PAT": 15174000000,
            "Free_Cash_Flow": 12500000000,
            "Period": "FY 2024",
            "Gross_Margin": "68.7%",
            "Operating_Margin": "27.5%"
        }
    },
    "Hermès": {
        "name": "Hermès International",
        "ticker": "RMS.PA",
        "exchange": "Euronext Paris",
        "currency": "EUR",
        "manual": {
            "Revenue": 13427000000,  # EUR 13.4B (FY2024)
            "EBITDA": 5894000000,
            "PBT": 5798000000,
            "PAT": 4308000000,
            "Free_Cash_Flow": 3800000000,
            "Period": "FY 2024",
            "Gross_Margin": "71.3%",
            "Operating_Margin": "42.0%"
        }
    },
    "Richemont": {
        "name": "Compagnie Financière Richemont",
        "ticker": "CFR.SW",
        "exchange": "SIX Swiss Exchange",
        "currency": "CHF",
        "manual": {
            "Revenue": 20643000000,  # CHF 20.6B (FY2024)
            "EBITDA": 5800000000,
            "PBT": 4156000000,
            "PAT": 3701000000,
            "Free_Cash_Flow": 2900000000,
            "Period": "FY 2024",
            "Gross_Margin": "64.5%",
            "Operating_Margin": "23.1%"
        }
    },
    "Watches of Switzerland": {
        "name": "Watches of Switzerland Group",
        "ticker": "WOSG.L",
        "exchange": "London Stock Exchange",
        "currency": "GBP",
        "manual": {
            "Revenue": 1652000000,  # GBP 1.65B (FY25)
            "EBITDA": 150000000,
            "PBT": 100000000,
            "PAT": 75000000,
            "Free_Cash_Flow": 98000000,
            "Period": "FY25 (Apr 27, 2025)",
            "Store_Count": 194,
            "Same_Store_Sales": "-6%",
            "Geographic_Mix": "UK: 45%, US: 55%",
            "Gross_Margin": "27.2%",
            "Operating_Margin": "9.1%"
        }
    },
    "The Hour Glass": {
        "name": "The Hour Glass Limited",
        "ticker": "AGS.SI",
        "exchange": "Singapore Exchange",
        "currency": "SGD",
        "manual": {
            "Revenue": 1162874000,  # SGD 1.16B (FY25)
            "EBITDA": 200000000,
            "PBT": 175432000,
            "PAT": 136083000,
            "Free_Cash_Flow": 120000000,
            "Period": "FY25 (Mar 31, 2025)",
            "Store_Count": 52,
            "Same_Store_Sales": "-14%",
            "Geographic_Mix": "SG: 45%, AU: 25%, Other: 30%",
            "Gross_Margin": "35.8%",
            "Operating_Margin": "15.1%"
        }
    }
}

# Dashboard title
st.title("💎 Luxury Retail Financial Dashboard")
st.markdown("**Top 5 Luxury Retail Companies - Live Financial Data (Alpha Vantage API)**")
st.markdown("---")

# ==============================================================================
# ALPHA VANTAGE API FUNCTIONS
# ==============================================================================

def format_number(value, currency="USD"):
    """Format numbers in millions/billions"""
    if value is None or pd.isna(value):
        return "N/A"
    try:
        value = float(value)
        if abs(value) >= 1e9:
            return f"{currency} {value/1e9:.2f}B"
        elif abs(value) >= 1e6:
            return f"{currency} {value/1e6:.2f}M"
        else:
            return f"{currency} {value:,.0f}"
    except:
        return str(value)

@st.cache_data(ttl=86400)  # Cache for 24 hours
def test_alpha_vantage_api():
    """Test if Alpha Vantage API key is working"""
    if ALPHA_VANTAGE_API_KEY == "YOUR_API_KEY_HERE":
        return False, "Not configured", None

    try:
        # Test with a simple quote endpoint
        test_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(test_url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if "Global Quote" in data and data["Global Quote"]:
                return True, "Connected", "IBM"
            elif "Error Message" in data:
                return False, "Invalid ticker format", None
            elif "Note" in data:
                return False, "Rate limit (25 calls/day)", None
            elif "Information" in data:
                return False, "Invalid API key", None
            else:
                return False, "Unknown response", None
        else:
            return False, f"HTTP {response.status_code}", None
    except Exception as e:
        return False, f"Connection failed", None

@st.cache_data(ttl=86400)  # Cache for 24 hours (data doesn't change often)
def get_alpha_vantage_data(ticker, company_key):
    """Fetch financial data from Alpha Vantage API"""

    if ALPHA_VANTAGE_API_KEY == "YOUR_API_KEY_HERE":
        return None

    try:
        # Alpha Vantage: Income Statement (Annual)
        income_url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"

        time.sleep(12)  # Alpha Vantage: 5 calls per minute = 12 seconds between calls

        income_response = requests.get(income_url, timeout=15)

        if income_response.status_code != 200:
            return None

        income_data = income_response.json()

        # Check for errors
        if "Error Message" in income_data or "Note" in income_data or "Information" in income_data:
            return None

        # Initialize data structure
        data = {
            "Company": COMPANIES[company_key]["name"],
            "Exchange": COMPANIES[company_key]["exchange"],
            "Currency": COMPANIES[company_key]["currency"],
            "Revenue": None,
            "EBITDA": None,
            "PBT": None,
            "PAT": None,
            "Free_Cash_Flow": None,
            "Period": "Latest",
            "Store_Count": None,
            "Same_Store_Sales": None,
            "Geographic_Mix": None,
            "Gross_Margin": None,
            "Operating_Margin": None
        }

        # Extract income statement data
        if "annualReports" in income_data and len(income_data["annualReports"]) > 0:
            latest = income_data["annualReports"][0]

            data["Revenue"] = float(latest.get("totalRevenue", 0)) if latest.get("totalRevenue") else None
            data["EBITDA"] = float(latest.get("ebitda", 0)) if latest.get("ebitda") else None
            data["PBT"] = float(latest.get("incomeBeforeTax", 0)) if latest.get("incomeBeforeTax") else None
            data["PAT"] = float(latest.get("netIncome", 0)) if latest.get("netIncome") else None
            data["Period"] = latest.get("fiscalDateEnding", "Latest")

            # Calculate margins
            if data["Revenue"] and data["Revenue"] > 0:
                gross_profit = float(latest.get("grossProfit", 0)) if latest.get("grossProfit") else None
                operating_income = float(latest.get("operatingIncome", 0)) if latest.get("operatingIncome") else None

                if gross_profit:
                    data["Gross_Margin"] = f"{(gross_profit / data['Revenue']) * 100:.1f}%"
                if operating_income:
                    data["Operating_Margin"] = f"{(operating_income / data['Revenue']) * 100:.1f}%"

        # Get Cash Flow data
        time.sleep(12)  # Rate limit

        cashflow_url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"
        cashflow_response = requests.get(cashflow_url, timeout=15)

        if cashflow_response.status_code == 200:
            cashflow_data = cashflow_response.json()

            if "annualReports" in cashflow_data and len(cashflow_data["annualReports"]) > 0:
                cash_latest = cashflow_data["annualReports"][0]

                operating_cf = float(cash_latest.get("operatingCashflow", 0)) if cash_latest.get("operatingCashflow") else None
                capex = float(cash_latest.get("capitalExpenditures", 0)) if cash_latest.get("capitalExpenditures") else None

                if operating_cf and capex:
                    data["Free_Cash_Flow"] = operating_cf - abs(capex)
                elif operating_cf:
                    data["Free_Cash_Flow"] = operating_cf

        # Add manual operational data
        if "manual" in COMPANIES[company_key]:
            manual = COMPANIES[company_key]["manual"]
            if "Store_Count" in manual:
                data["Store_Count"] = manual["Store_Count"]
            if "Same_Store_Sales" in manual:
                data["Same_Store_Sales"] = manual["Same_Store_Sales"]
            if "Geographic_Mix" in manual:
                data["Geographic_Mix"] = manual["Geographic_Mix"]

        # Return if we got some data
        if data["Revenue"] or data["PAT"]:
            return data
        else:
            return None

    except Exception as e:
        return None

def get_manual_data(company_key):
    """Get manual fallback data"""
    company = COMPANIES[company_key]

    if "manual" in company:
        return {
            "Company": company["name"],
            "Exchange": company["exchange"],
            "Currency": company["currency"],
            **company["manual"]
        }
    return None

# ==============================================================================
# SIDEBAR CONTROLS
# ==============================================================================
st.sidebar.header("🎛️ Dashboard Controls")

# API Status Check
st.sidebar.markdown("### 🔑 API Status")

if ALPHA_VANTAGE_API_KEY == "YOUR_API_KEY_HERE":
    st.sidebar.error("❌ Not Configured")
    st.sidebar.info("📝 Edit app.py line 21")
    st.sidebar.markdown("[Get Free Key →](https://www.alphavantage.co/support/#api-key)")
    api_ok = False
    use_api = False
else:
    api_ok, api_msg, test_symbol = test_alpha_vantage_api()

    if api_ok:
        st.sidebar.success(f"✅ {api_msg}")
        if test_symbol:
            st.sidebar.caption(f"Test: {test_symbol}")
    else:
        st.sidebar.warning(f"⚠️ {api_msg}")

    # Let user choose data source
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Data Source")

    data_source = st.sidebar.radio(
        "Choose:",
        ["Use API (Dynamic)", "Use Manual Data Only"],
        index=0 if api_ok else 1
    )

    use_api = (data_source == "Use API (Dynamic)" and api_ok)

st.sidebar.markdown("---")

# Display options
st.sidebar.markdown("### 🎨 Display")
show_operational = st.sidebar.checkbox("Show Operational Metrics", value=True)
show_debug = st.sidebar.checkbox("Show Debug Info", value=False)

# Refresh button
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown(f"*Updated: {datetime.now().strftime('%H:%M')}*")

# API info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 API Limits")
st.sidebar.caption("Free: 25 calls/day")
st.sidebar.caption("5 companies = 10 calls")
st.sidebar.caption("Rate: 5 calls/min")
st.sidebar.caption("Cache: 24 hours")

# ==============================================================================
# FETCH DATA
# ==============================================================================

if use_api:
    st.info("⏳ Fetching live data from Alpha Vantage... This takes ~2 minutes due to rate limits (5 calls/min)")
    progress_bar = st.progress(0)
    status_text = st.empty()

with st.spinner("Loading financial data..."):
    all_data = []
    api_status = []
    total_companies = len(COMPANIES)

    for idx, (key, company) in enumerate(COMPANIES.items()):
        data = None
        status = "⏳"

        if use_api:
            status_text.text(f"Fetching {company['name']}... ({idx+1}/{total_companies})")

            data = get_alpha_vantage_data(company["ticker"], key)

            if data and data.get("Revenue"):
                status = "✅ API"
                api_status.append(f"{company['name']}: Live data from API")
            else:
                status = "📝 Manual"
                data = get_manual_data(key)
                api_status.append(f"{company['name']}: Using manual fallback")

            progress_bar.progress((idx + 1) / total_companies)
        else:
            # Use manual data
            data = get_manual_data(key)
            status = "📝 Manual"
            api_status.append(f"{company['name']}: Manual data (API not used)")

        if data:
            all_data.append(data)

if use_api:
    progress_bar.empty()
    status_text.empty()

# Debug info
if show_debug and api_status:
    with st.expander("🔍 Debug Information"):
        for status in api_status:
            st.text(status)

# ==============================================================================
# DISPLAY DASHBOARD
# ==============================================================================

if all_data and len(all_data) > 0:
    df = pd.DataFrame(all_data)

    # Financial Metrics
    st.header("📊 Financial Metrics")

    fin_cols = ["Company", "Exchange", "Currency", "Revenue", "EBITDA", "PBT", "PAT", "Free_Cash_Flow", "Period"]
    fin_df = df[fin_cols].copy()

    for col in ["Revenue", "EBITDA", "PBT", "PAT", "Free_Cash_Flow"]:
        fin_df[col] = fin_df.apply(lambda row: format_number(row[col], row["Currency"]), axis=1)

    st.dataframe(fin_df, use_container_width=True, hide_index=True)

    # Operational Metrics
    if show_operational:
        st.header("🏪 Operational Metrics")
        ops_cols = ["Company", "Store_Count", "Same_Store_Sales", "Geographic_Mix", "Gross_Margin", "Operating_Margin"]
        ops_df = df[ops_cols].copy().fillna("N/A")
        st.dataframe(ops_df, use_container_width=True, hide_index=True)

    # Key Insights
    st.header("💡 Key Insights")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Companies", len(df))
    with col2:
        total_rev = df["Revenue"].apply(lambda x: x if pd.notna(x) else 0).sum()
        st.metric("Total Revenue", format_number(total_rev, "Mixed"))
    with col3:
        st.metric("Exchanges", df["Exchange"].nunique())

    # Export
    st.header("📥 Export Data")
    export_df = pd.concat([fin_df, ops_df.drop(columns=["Company"]) if show_operational else pd.DataFrame()], axis=1)
    csv = export_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📊 Download CSV",
        csv,
        f"luxury_dashboard_{datetime.now().strftime('%Y%m%d')}.csv",
        "text/csv",
        use_container_width=True
    )
else:
    st.error("⚠️ No Data Available")
    st.info("""
    **Quick Fixes:**
    1. Add Alpha Vantage API key at line 21
    2. Get free key: https://www.alphavantage.co/support/#api-key
    3. Or use "Manual Data Only" in sidebar
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p><strong>Luxury Retail Financial Dashboard</strong></p>
    <p>Powered by Alpha Vantage API • Free Tier: 25 calls/day</p>
    <p style='font-size: 0.8em;'>Data refreshes daily • Manual fallback available</p>
</div>
""", unsafe_allow_html=True)
