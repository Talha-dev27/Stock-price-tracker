# 📌 Stock Price Tracker App (with Step-by-Step Instructions)



import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
import smtplib

# ---------- EMAIL ALERT FUNCTION ----------
def send_email_alert(symbol, current_price, target_price, email):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        sender_email = "your_email@gmail.com"
        password = "your_app_password"   # Use Gmail App Passwords

        server.login(sender_email, password)
        subject = f"Stock Alert: {symbol}"
        body = f"{symbol} crossed your target price of ${target_price}.\nCurrent Price: ${current_price:.2f}"
        msg = f"Subject: {subject}\n\n{body}"

        server.sendmail(sender_email, email, msg)
        server.quit()
    except Exception as e:
        st.error(f"Email alert failed: {e}")


# ---------- STREAMLIT APP ----------
st.title("📈 Advanced Stock Price Tracker")

# Input for multiple stocks
symbols = st.text_input("Enter Stock Symbols (comma separated, e.g. AAPL, TSLA, MSFT):", "AAPL, TSLA")

# Target price alert
target_price = st.number_input("Set Target Price for Alerts (USD):", min_value=0.0, value=200.0)
alert_email = st.text_input("Enter your email for alerts (optional):")

if st.button("Track Stocks"):
    symbols = [s.strip().upper() for s in symbols.split(",")]

    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1mo")

            if not data.empty:
                current_price = data["Close"].iloc[-1]

                st.subheader(f"📊 {symbol} - Current Price: ${current_price:.2f}")

                # Stock extra info
                info = stock.info
                st.write({
                    "Market Cap": info.get("marketCap", "N/A"),
                    "P/E Ratio": info.get("trailingPE", "N/A"),
                    "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
                    "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
                })

                # Alert check
                if current_price >= target_price and alert_email:
                    send_email_alert(symbol, current_price, target_price, alert_email)
                    st.success(f"🚨 ALERT SENT! {symbol} crossed ${target_price}.")

                # Plot price trend
                fig, ax = plt.subplots()
                ax.plot(data.index, data["Close"], label="Closing Price")
                ax.set_xlabel("Date")
                ax.set_ylabel("Price (USD)")
                ax.legend()
                st.pyplot(fig)

            else:
                st.warning(f"No data found for {symbol}. Try another one.")
        except Exception as e:
            st.error(f"Error fetching {symbol}: {e}")
import streamlit as st

st.title("📈 Stock Price Tracker")
st.write("Hello! If you see this, Streamlit is working ✅")
