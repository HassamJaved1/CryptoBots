
# from binance.client import Client
# import pandas as pd
# import time


# client = Client(api_key, api_secret)

 


# # Trading pair and interval


# TRADING_PAIR = 'DOGEUSDT'  # Example: Bitcoin vs. US Dollar Tether
# INTERVAL = Client.KLINE_INTERVAL_1MINUTE  # Candle interval (1-minute for testing)

# # Parameters for moving averages
# SHORT_WINDOW = 9   # Short-term MA (Fast)
# LONG_WINDOW = 21   # Long-term MA (Slow)

# def get_historical_data(symbol, interval, lookback):
#     """Fetch historical candlestick data and return as a pandas DataFrame."""
#     klines = client.get_klines(symbol=symbol, interval=interval, limit=lookback)
#     df = pd.DataFrame(klines, columns=[
#         "timestamp", "open", "high", "low", "close", "volume", 
#         "close_time", "quote_asset_volume", "trades", 
#         "taker_buy_base", "taker_buy_quote", "ignore"
#     ])
#     df["close"] = df["close"].astype(float)
#     return df[["timestamp", "close"]]

# def calculate_moving_averages(data):
#     """Calculate short-term and long-term moving averages."""
#     data['SMA_Short'] = data['close'].rolling(window=SHORT_WINDOW).mean()
#     data['SMA_Long'] = data['close'].rolling(window=LONG_WINDOW).mean()
#     return data

# def check_signals(data):
#     """Generate buy/sell signals based on moving averages."""
#     # Get the last two rows to check for crossover
#     short_ma = data['SMA_Short'].iloc[-2:]
#     long_ma = data['SMA_Long'].iloc[-2:]

#     if short_ma.iloc[0] < long_ma.iloc[0] and short_ma.iloc[1] > long_ma.iloc[1]:
#         return "Buy"
#     elif short_ma.iloc[0] > long_ma.iloc[0] and short_ma.iloc[1] < long_ma.iloc[1]:
#         return "Sell"
#     else:
#         return "Hold"

# def main():
#     """Main trading loop."""
#     try:
#         while True:
#             # Fetch historical data
#             print("Fetching data...")
#             data = get_historical_data(TRADING_PAIR, INTERVAL, lookback=LONG_WINDOW + 1)
            
#             # Calculate moving averages
#             data = calculate_moving_averages(data)
            
#             # Check signals
#             signal = check_signals(data)
#             print(f"Latest Signal: {signal}")
            
#             # Wait before fetching new data
#             time.sleep(20)  # Adjust based on the selected interval

#     except KeyboardInterrupt:
#         print("Trading bot stopped.")

# # Run the bot
# if __name__ == "__main__":
#     main()





# THIS IS THE IMPROVED CODE

from binance.client import Client
import pandas as pd
import winsound
import time


api_key = ""
api_secret = ""
client = Client(api_key, api_secret)


# Trading pair and interval
TRADING_PAIR = 'EIGENUSDT'
INTERVAL = Client.KLINE_INTERVAL_1MINUTE  # Candle interval

# Moving Average Parameters
SHORT_WINDOW = 9  # Short-term MA (Fast)
LONG_WINDOW = 21  # Long-term MA (Slow)

# Risk Management Parameters
TRADE_AMOUNT = 50  # USD value to trade per transaction
STOP_LOSS_PERCENT = 0.02  # 2% below buy price
TAKE_PROFIT_PERCENT = 0.05  # 5% above buy price

# Log file
LOG_FILE = "trading_log.txt"

def log_message(message):
    """Log a message to the console and to a file."""
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def get_historical_data(symbol, interval, lookback):
    """Fetch historical candlestick data and return as a pandas DataFrame."""
    klines = client.get_klines(symbol=symbol, interval=interval, limit=lookback)
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    return df[["timestamp", "close"]]

def calculate_moving_averages(data):
    """Calculate short-term and long-term moving averages."""
    data['SMA_Short'] = data['close'].rolling(window=SHORT_WINDOW).mean()
    data['SMA_Long'] = data['close'].rolling(window=LONG_WINDOW).mean()
    return data

def check_signals(data):
    """Generate buy/sell signals based on moving averages."""
    short_ma = data['SMA_Short'].iloc[-2:]
    long_ma = data['SMA_Long'].iloc[-2:]

    if short_ma.iloc[0] < long_ma.iloc[0] and short_ma.iloc[1] > long_ma.iloc[1]:
        return "Buy"
    elif short_ma.iloc[0] > long_ma.iloc[0] and short_ma.iloc[1] < long_ma.iloc[1]:
        return "Sell"
    else:
        return "Hold"

def execute_trade(signal, trading_pair, trade_amount):
    """Execute a trade based on the signal"""
    if signal == "Buy":
        # Place a market buy order
        price = float(client.get_symbol_ticker(symbol=trading_pair)['price'])
        quantity = round(trade_amount / price, 5)  # Calculate quantity to buy
        order = client.order_market_buy(symbol=trading_pair, quantity=quantity)
        log_message(f"Buy order placed: {order}")
        return "Bought", price
    elif signal == "Sell":
        # Place a market sell order (sell everything)
        balance = float(client.get_asset_balance(asset=trading_pair[:-4])['free'])
        if balance > 0:
            order = client.order_market_sell(symbol=trading_pair, quantity=balance)
            log_message(f"Sell order placed: {order}")
            return "Sold", None
    return None, None

def main():
    """Main trading loop."""
    try:
        buy_price = None
        while True:
            log_message("Fetching data...")
            data = get_historical_data(TRADING_PAIR, INTERVAL, lookback=LONG_WINDOW + 1)
            data = calculate_moving_averages(data)
            signal = check_signals(data)
            log_message(f"Signal: {signal}")

                
            # Execute trades based on signals`
            if signal == "Buy": #and buy_price is None:
                print("Buy this coin")
                # status, buy_price = execute_trade(signal, TRADING_PAIR, TRADE_AMOUNT)

            elif signal == "Sell":
               winsound.Beep(1000, 500)
               print("Sell  this coin")
                #and buy_price is not None:
                # status, _ = execute_trade(signal, TRADING_PAIR, TRADE_AMOUNT)
                # if status == "Sold":
                #     buy_price = None

            # # Check for stop-loss or take-profit
            # if buy_price:
            #     current_price = float(client.get_symbol_ticker(symbol=TRADING_PAIR)['price'])
            #     if current_price <= buy_price * (1 - STOP_LOSS_PERCENT):
            #         log_message("Stop-loss triggered. Selling position.")
            #         execute_trade("Sell", TRADING_PAIR, TRADE_AMOUNT)
            #         buy_price = None
            #     elif current_price >= buy_price * (1 + TAKE_PROFIT_PERCENT):
            #         log_message("Take-profit triggered. Selling position.")
            #         execute_trade("Sell", TRADING_PAIR, TRADE_AMOUNT)
            #         buy_price = None

            # time.sleep(20)  # Adjust based on interval

    except KeyboardInterrupt:
        log_message("Trading bot stopped by user.")
    except Exception as e:
        log_message(f"Error: {e}")

# Run the bot
if __name__ == "__main__":
    main()