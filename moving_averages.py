

  ## Fetch historical data
# def get_historical_data(symbol, interval):
#     klines = client.get_historical_klines(symbol, interval, "1 month ago UTC")
#     df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
#                                        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
#                                        'taker_buy_quote_asset_volume', 'ignore'])
#     df['close'] = df['close'].astype(float)
#     return df

# # Calculate RSI
# def calculate_rsi(data, period=14):
#     delta = data['close'].diff()
#     gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
#     loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
#     rs = gain / loss
#     rsi = 100 - (100 / (1 + rs))
#     data['RSI'] = rsi
#     return data

# # Execute trading strategy
# def rsi_strategy(symbol, interval, oversold=30, overbought=70):
#     data = get_historical_data(symbol, interval)
#     data = calculate_rsi(data)
    
#     # Get the latest RSI
#     latest_rsi = data['RSI'].iloc[-1]
#     print(f"Latest RSI: {latest_rsi}")
    
#     if latest_rsi < oversold:
#         print("RSI indicates oversold. Placing a BUY order.")
#     elif latest_rsi > overbought:
#         print("RSI indicates overbought. Placing a SELL order.")
       
#     else:
#         print("No action taken.")

# # Run the bot
# rsi_strategy("ETHUSDT", Client.KLINE_INTERVAL_1HOUR)
