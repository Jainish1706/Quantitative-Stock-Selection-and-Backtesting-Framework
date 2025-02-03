def calculate_buy_sell_tags(daily_data):
    buy_results = []
    sell_results = []

    daily_data['ATR'] = ta.atr(daily_data['High'], daily_data['Low'], daily_data['Close'], timeperiod=14)

    for index, row in daily_data.iterrows():
        date = pd.to_datetime(row['Date'])


        # Indicators
        current_price = (row['Open'] + row['Close']) / 2
        sma_200 = row['VWSMA_200']  # 200-day SMA
        ema_50 = row['VWEMA_50']  # 50-day EMA
        ema_20 = row['VWEMA_20']
        rsi = row['RSI_Daily']

        # Buy Logic: Trend + Volatility Breakout + RSI
        if (current_price > sma_200 and
            current_price > ema_50 and 
            current_price > ema_20 and
            rsi < 70):  # Ensure RSI is not overbought  and #
            buy_results.append((row['Date'], 1))
        else:
            buy_results.append((row['Date'], 0))

        # Sell Logic: Trend Reversal + RSI + ATR Stop
        if (current_price < ema_50 or
            rsi > 70):  # ATR-based trailing stop
            sell_results.append((row['Date'], 1))
        else:
            sell_results.append((row['Date'], 0))

    return buy_results, sell_results


# Function to generate transactions and calculate returns
def generate_transactions(daily_data, result_df, script):
    transactions = []
    holding = False  # Track whether we currently hold a position
    buy_date = None
    buy_price = None

    for index, row in result_df.iterrows():
        if row['Buy_Tag'] == 1 and not holding:
            # Record the buy date and price
            buy_date = row['Date']
            buy_row = daily_data[daily_data['Date'] == buy_date].iloc[0]
            buy_price = (buy_row['Open'] + buy_row['Close']) / 2
            holding = True  # We are now holding a position

        elif row['Sell_Tag'] == 1 and holding:
            # Record the sell date and price
            sell_date = row['Date']
            sell_row = daily_data[daily_data['Date'] == sell_date].iloc[0]
            sell_price = (sell_row['Open'] + sell_row['Close']) / 2

            # Calculate transaction return and store it
            transaction_return = sell_price - buy_price
            transactions.append((script, buy_date, sell_date, transaction_return))

            # Reset holding flag
            holding = False

    # Return the transactions as a DataFrame
    return pd.DataFrame(transactions, columns=['Script', 'Buy_Date', 'Sell_Date', 'Return'])