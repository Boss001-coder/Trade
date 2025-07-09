def detect_trend(prices):
    change = prices[-1] - prices[0]
    if change > 0.01 * prices[0]:
        return "Uptrend 📈"
    elif change < -0.01 * prices[0]:
        return "Downtrend 📉"
    else:
        return "Sideways ➖"
