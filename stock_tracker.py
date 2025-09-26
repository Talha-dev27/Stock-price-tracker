import streamlit as st
import yfinance as yf

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="My Stock Tracker",
    page_icon="📈",
    layout="wide"
)

# ---------------- Custom Header ----------------
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

selected_stock = st.sidebar.selectbox("Choose a Stock", list(stock_options.keys()))
ticker = stock_options[selected_stock]

# Time and interval options
period = st.sidebar.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y", "5y", "max"])
interval = st.sidebar.selectbox("Select Interval", ["1d", "1wk", "1mo"])

# ---------------- Fetch Data ----------------
try:
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)

    if data.empty:
        st.error("⚠️ No data found. Try another stock.")
    else:
        # ---------------- Layout ----------------
        col1, col2 = st.columns([2, 3])

        with col1:
            st.subheader(f"📌 {ticker} Data")
            st.dataframe(data.tail(10))  # last 10 rows

        with col2:
            st.subheader(f"📈 {ticker} Closing Price Chart")
            st.line_chart(data["Close"])

        st.success(f"✅ Successfully loaded data for {ticker}")

except Exception as e:
    st.error(f"❌ Error: {e}")
