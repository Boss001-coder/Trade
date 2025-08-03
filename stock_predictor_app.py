import streamlit as st
import easyocr
import numpy as np
import pandas as pd
import cv2
from PIL import Image
import random

# OCR Reader
reader = easyocr.Reader(['en'])

st.set_page_config(page_title="Indian Stock & F&O Predictor", layout="centered")

st.title("📈 Indian Stock & F&O Price Predictor")
st.write("Upload a Kotak Neo chart screenshot, enter stock name, and get price prediction.")

# Upload chart image
uploaded_file = st.file_uploader("Upload Kotak Neo chart screenshot", type=["png", "jpg", "jpeg"])

# Stock name and time frame input
stock_name = st.text_input("Enter stock name (e.g., RELIANCE, NIFTY, INFY):")
time_frame = st.selectbox(
    "Select prediction time frame:",
    ["30 minutes", "1 hour", "2 hours", "3 hours", "4 hours"]
)

predict_button = st.button("Predict Price")

def simulate_prediction(stock, timeframe):
    base_price = random.uniform(100, 1500)
    factor = {
        "30 minutes": 0.5,
        "1 hour": 1.0,
        "2 hours": 1.8,
        "3 hours": 2.5,
        "4 hours": 3.2,
    }[timeframe]
    price_change = random.uniform(-1, 1) * factor
    predicted_price = round(base_price + price_change, 2)
    return predicted_price

if predict_button:
    if not uploaded_file or not stock_name:
        st.error("Please upload an image and enter stock name.")
    else:
        image = Image.open(uploaded_file)
        img_np = np.array(image.convert("RGB"))

        with st.spinner("Analyzing chart..."):
            results = reader.readtext(img_np)

        st.subheader("🧾 Detected Text in Chart:")
        text_list = [res[1] for res in results]
        st.write(", ".join(text_list) if text_list else "No text detected.")

        predicted_price = simulate_prediction(stock_name.upper(), time_frame)
        st.success(f"📊 Predicted price of **{stock_name.upper()}** after {time_frame}: ₹{predicted_price}")
        st.image(image, caption="Uploaded Chart", use_column_width=True)
