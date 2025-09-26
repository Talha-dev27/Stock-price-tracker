import streamlit as st
import yfinance as yf
import pandas as pd

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="My Stock Tracker",
    page_icon="📈",
    layout="wide"
)

# ---------------- Header ----------------
st.title("📊 My Custom Stock Tracker")
st.markdown("Track your favorite stocks with style 🚀")

# ---------------- Sidebar ----------------
st.sidebar.header("⚙️ Settings")

# Predefined stock options
stock_options = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Google (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Tesla (TSLA)": "TSLA",
    "Meta (META)": "META",
    "Nvidia (NVDA)": "NVDA",
    "Netflix (NFLX)": "NFLX"
}

# Dropdown or custom input
selected_stock = st.sidebar.selectbox("Choose a Stock", list(stock_options.keys()))
ticker = stock_options[selected_stock]
custom_ticker = st.sidebar.text_input("Or enter custom ticker (e.g. IBM)")

if custom_ticker:
    ticker = custom_ticker.upper()

# Time and interval options
period = st.sidebar.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y", "5y", "max"])
interval = st.sidebar.selectbox("Select Interval", ["1d", "1wk", "1mo"])

# Multiple stock comparison
compare_stocks = st.sidebar.multiselect("Compare with other stocks", list(stock_options.keys()))

# ---------------- Fetch Data ----------------
try:
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)

    if data.empty:
        st.error("⚠️ No data found. Try another stock.")
    else:
        # ---------------- Stock Info ----------------
        info = stock.info
        st.subheader(f"ℹ️ {ticker} Stock Information")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
        with col2:
            st.metric("Market Cap", f"${info.get('marketCap', 'N/A'):,}")
        with col3:
            st.metric("P/E Ratio", info.get("trailingPE", "N/A"))

        # ---------------- Layout ----------------
        col1, col2 = st.columns([2, 3])

        with col1:
            st.subheader(f"📌 {ticker} Data")
            st.dataframe(data.tail(10))  # last 10 rows

        with col2:
            st.subheader(f"📈 {ticker} Closing Price Chart")
            st.line_chart(data["Close"])

        # ---------------- Comparison Chart ----------------
        if compare_stocks:
            st.subheader("📊 Stock Comparison")
            compare_dict = {ticker: data["Close"]}

            for stock_name in compare_stocks:
                comp_ticker = stock_options[stock_name]
                comp_data = yf.Ticker(comp_ticker).history(period=period, interval=interval)
                if not comp_data.empty:
                    compare_dict[comp_ticker] = comp_data["Close"]

            compare_df = pd.DataFrame(compare_dict)
            st.line_chart(compare_df)

        st.success(f"✅ Successfully loaded data for {ticker}")

except Exception as e:
    st.error(f"❌ Error: {e}")
