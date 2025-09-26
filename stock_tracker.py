import streamlit as st
import yfinance as yf
import pandas as pd

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="My Stock Tracker",
    page_icon="📈",
    layout="wide"
)

# ---------------- Sidebar ----------------
st.sidebar.header("⚙️ Settings")

# Page Navigation
page = st.sidebar.radio("Navigate", ["📊 Analysis", "📈 Chart", "📋 Data Table"])

# Predefined stock options
stock_options = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Google (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Tesla (TSLA)": "TSLA",
    "Meta (META)": "META",
    "Nvidia (NVDA)": "NVDA",
    "Netflix (NFLX)": "NFLX",
    "Coca-Cola (KO)": "KO",
    "Intel (INTC)": "INTC",
    "AMD (AMD)": "AMD"
}

selected_stock = st.sidebar.selectbox("Choose a Stock", list(stock_options.keys()))
ticker = stock_options[selected_stock]

# Time and interval options
period = st.sidebar.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y", "5y", "max"])
interval = st.sidebar.selectbox("Select Interval", ["1d", "1wk", "1mo"])

# Theme toggle
theme = st.sidebar.radio("Theme", ["🌞 Light", "🌙 Dark"])

# Custom CSS for themes
if theme == "🌙 Dark":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------- Fetch Data ----------------
try:
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)

    if data.empty:
        st.error("⚠️ No data found. Try another stock.")
    else:
        # ---------------- Analysis Page ----------------
        if page == "📊 Analysis":
            st.title(f"📈 {ticker} Stock Analysis")

            info = stock.info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
            with col2:
                st.metric("Market Cap", f"${info.get('marketCap', 0):,}")
            with col3:
                st.metric("P/E Ratio", info.get("trailingPE", "N/A"))

        # ---------------- Chart Page ----------------
        elif page == "📈 Chart":
            st.title(f"📉 {ticker} Stock Price Chart")
            st.line_chart(data["Close"])

        # ---------------- Data Table Page ----------------
        elif page == "📋 Data Table":
            st.title(f"📊 {ticker} Historical Data")
            st.dataframe(data.tail(20))

        st.success(f"✅ Successfully loaded data for {ticker}")

except Exception as e:
    st.error(f"❌ Error: {e}")
