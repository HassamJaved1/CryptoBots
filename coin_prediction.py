
import pandas as pd
import numpy as np
from binance.client import Client

# Initialize Binance Client

api_key = ""
api_secret = ""
client = Client(api_key, api_secret)

# Fetch all symbols traded against USDT (spot market only)
def fetch_all_usdt_pairs():
    """
    Fetch all trading pairs against USDT available on Binance.
    """
    exchange_info = client.get_exchange_info()
    symbols = [
        symbol["symbol"] for symbol in exchange_info["symbols"]
        if symbol["quoteAsset"] == "USDT" and symbol["status"] == "TRADING"
    ]
    return symbols

# Fetch historical candlestick data
def fetch_klines(symbol, interval, limit=100):
    """
    Fetch historical kline (candlestick) data for a given symbol and interval.
    """
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume", "close_time",
        "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume", "ignore"
    ])
    df["close"] = pd.to_numeric(df["close"])
    return df

# Calculate RSI
def calculate_rsi(data, period=14):
    """
    Calculate Relative Strength Index (RSI) for a given price data.
    """
    delta = data["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate moving averages
def calculate_moving_averages(data, short_window=9, long_window=21):
    """
    Calculate short and long-term moving averages.
    """
    data["SMA_Short"] = data["close"].rolling(window=short_window).mean()
    data["SMA_Long"] = data["close"].rolling(window=long_window).mean()
    return data

# Analyze a single symbol
def analyze_coin(symbol):
    """
    Analyze a single coin for potential buy signals.
    """
    try:
        df = fetch_klines(symbol, interval="15m")  # 15-minute interval for short-term trading
        df = calculate_moving_averages(df)
        df["RSI"] = calculate_rsi(df)

        latest_data = df.iloc[-1]
        previous_data = df.iloc[-2]

        # Trading Signals
        buy_signal = (
            (latest_data["SMA_Short"] > latest_data["SMA_Long"]) and
            (previous_data["SMA_Short"] <= previous_data["SMA_Long"]) and
            (latest_data["RSI"] < 70)  # RSI not in overbought zone
        )

        if buy_signal:
            return f"BUY Signal for {symbol}: Price = {latest_data['close']}, RSI = {latest_data['RSI']:.2f}"
        else:
            return f"No BUY Signal for {symbol}. Current RSI = {latest_data['RSI']:.2f}"

    except Exception as e:
        return f"Error analyzing {symbol}: {e}"

# Analyze all coins
def main():
    """
    Main function to analyze all coins and suggest which ones to buy.
    """
    print("Fetching all trading pairs against USDT...")
    coins = fetch_all_usdt_pairs()
    print(f"Found {len(coins)} USDT trading pairs.")

    print("\nAnalyzing coins for short-term trading...\n")
    recommendations = []
    for coin in coins:
        recommendation = analyze_coin(coin)
        recommendations.append(recommendation)
        print(recommendation)

    print("\nAnalysis Complete.")
    return recommendations

if __name__ == "__main__":
    main()