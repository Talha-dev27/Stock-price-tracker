# stock_tracker.py
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import requests

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="My Stock Tracker",
    page_icon="📈",
    layout="wide"
)

# ---------------- Sidebar / Settings ----------------
st.sidebar.header("⚙️ Settings")

# Theme selection
theme = st.sidebar.radio("Choose Theme", ["Dark", "Light", "Custom"])
if theme == "Dark":
    chart_theme = "plotly_dark"
elif theme == "Light":
    chart_theme = "plotly_white"
else:
    chart_theme = "plotly"

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
    "SPY (SPY)": "SPY",
    "Bitcoin (BTC-USD)": "BTC-USD"
}

selected_stock = st.sidebar.selectbox("Choose a Stock", list(stock_options.keys()))
ticker = stock_options[selected_stock]
custom_ticker = st.sidebar.text_input("Or enter custom ticker (e.g. IBM)")

if custom_ticker:
    ticker = custom_ticker.strip().upper()

# Time and interval options
period = st.sidebar.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y", "5y", "max"])
interval = st.sidebar.selectbox("Select Interval", ["1d", "1wk", "1mo"])

# Multiple stock comparison (select from predefined list)
compare_stocks = st.sidebar.multiselect("Compare with other stocks", list(stock_options.keys()))

# Page Navigation
page = st.sidebar.radio("Navigation", ["📊 Analysis", "📰 News"])

# ---------------- Helpers ----------------
def fmt_number(x):
    if x is None:
        return "N/A"
    try:
        return f"{int(x):,}"
    except Exception:
        try:
            return f"{float(x):,}"
        except Exception:
            return str(x)

# ---------------- Fetch Data ----------------
try:
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)

    if data is None or data.empty:
        st.error("⚠️ No data found. Try another stock or a different period/interval.")
    else:
        # ---------------- Analysis Page ----------------
        if page == "📊 Analysis":
            st.title(f"📈 {ticker} Stock Analysis")

            # Stock basic info (use info safely)
            info = {}
            try:
                info = stock.info or {}
            except Exception:
                info = {}

            current_price = info.get("currentPrice") or (data_


