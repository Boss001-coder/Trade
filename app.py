import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from lstm_model import create_lstm_model, prepare_data
from trend import detect_trend
import numpy as np

st.set_page_config(page_title="📊 Stock AI Trend & Prediction", layout="centered")

st.title("📉 AI Stock Trend & Price Predictor")

# Option: Upload File or Enter Ticker
option = st.radio("Choose input type:", ["📁 Upload Chart Screenshot (CSV)", "🌐 Online (Yahoo Finance)"])

if option == "📁 Upload Chart Screenshot (CSV)":
    file = st.file_uploader("Upload CSV file with Date and Close columns", type=["csv"])
    if file:
        df = pd.read_csv(file)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        close = df['Close'].values
        st.line_chart(df.set_index('Date')['Close'])

elif option == "🌐 Online (Yahoo Finance)":
    ticker = st.text_input("Enter stock ticker (e.g. AAPL):", "AAPL")
    if ticker:
        df = yf.download(ticker, period='1y')
        close = df['Close'].values
        st.line_chart(df['Close'])

# Trend detection
if 'close' in locals() and len(close) > 60:
    trend = detect_trend(close[-60:])
    st.subheader(f"📌 Detected Trend: {trend}")

    # Prepare and predict
    X, y, scaler = prepare_data(close)
    model = create_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=5, batch_size=32, verbose=0)

    pred = model.predict(X)
    predicted_prices = scaler.inverse_transform(pred)

    # Show chart
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(close[-len(predicted_prices):], label='Actual')
    ax.plot(predicted_prices, label='Predicted')
    ax.set_title("Price Prediction")
    ax.legend()
    st.pyplot(fig)
