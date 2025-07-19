import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from trend import detect_trend
from PIL import Image

st.set_page_config(page_title="📊 Stock Intraday Trend Analyzer", layout="centered")
st.title("📉 Stock Chart + Trend Detector (Intraday)")

option = st.radio("Choose input type:", ["📁 Upload CSV", "🌐 Online Ticker", "🖼️ Upload Chart Screenshot"])

if option == "📁 Upload CSV":
    file = st.file_uploader("Upload CSV with 'Date' or 'Datetime' and 'Close'", type=["csv"])
    if file:
        df = pd.read_csv(file)

        # Flexible date column handling
        date_col = 'Date' if 'Date' in df.columns else ('Datetime' if 'Datetime' in df.columns else None)
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col])
            df = df.rename(columns={date_col: 'Date'})
            df = df.sort_values('Date')
            close = df['Close'].values
            st.line_chart(df.set_index('Date')['Close'])

            if len(close) > 10:
                trend = detect_trend(close[-60:] if len(close) > 60 else close)
                st.subheader(f"📌 Detected Trend: {trend}")
        else:
            st.error("CSV must contain a 'Date' or 'Datetime' column.")

elif option == "🌐 Online Ticker":
    ticker = st.text_input("Enter stock ticker (e.g. AAPL, ^NSEI):", "AAPL")
    interval = st.selectbox("Select interval", ["1m", "5m", "15m"])
    hours = st.selectbox("Time Window", ["30 minutes", "1 hour", "2 hours"])
    multiplier = {"30 minutes": 30, "1 hour": 60, "2 hours": 120}
    if ticker:
        df = yf.download(ticker, period='1d', interval=interval)
        close = df['Close'].values
        st.line_chart(df['Close'])

        if len(close) >= multiplier[hours]:
            trend = detect_trend(close[-multiplier[hours]:])
            st.subheader(f"📌 {hours} Trend: {trend}")
        else:
            st.warning("Not enough data for selected time window.")

elif option == "🖼️ Upload Chart Screenshot":
    img = st.file_uploader("Upload chart image (JPG, PNG)", type=["jpg", "png"])
    if img:
        image = Image.open(img)
        st.image(image, caption="Uploaded Chart", use_column_width=True)
        st.info("Currently only for viewing. Trend detection from image not supported yet.")
