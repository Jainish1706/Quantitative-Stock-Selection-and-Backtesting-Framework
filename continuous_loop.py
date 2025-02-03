def closed_loop(Init_amt, Weights, stock_list, folder_path, result_dfs):
    scripts = [stock.split('.')[0] for stock in stock_list]  # Remove ".NS"
    money_alloted = {scripts[i]: Init_amt * Weights[i] for i in range(len(scripts))}
    total_portfolio_value = Init_amt  # Track total portfolio value

    transactions = []  # Store transactions for tracking

    for script in scripts:
        # Load stock's daily data
        daily_data = pd.read_csv(f'{folder_path}/Daily/{script}_Daily.csv')

        # Use precomputed result_df instead of reading from CSV
        result_df = result_dfs[script]

        holding = False
        buy_price = None
        shares_bought = 0

        for index, row in result_df.iterrows():
            if row['Buy_Tag'] == 1 and not holding:
                buy_date = row['Date']
                buy_row = daily_data[daily_data['Date'] == buy_date]

                if not buy_row.empty:
                    buy_price = (buy_row.iloc[0]['Open'] + buy_row.iloc[0]['Close']) / 2
                    shares_bought = money_alloted[script] / buy_price  # Calculate shares
                    holding = True  # Mark as holding position

            elif row['Sell_Tag'] == 1 and holding:
                sell_date = row['Date']
                sell_row = daily_data[daily_data['Date'] == sell_date]

                if not sell_row.empty:
                    sell_price = (sell_row.iloc[0]['Open'] + sell_row.iloc[0]['Close']) / 2
                    trade_profit = shares_bought * (sell_price - buy_price)

                    # Update money allotted to this stock
                    money_alloted[script] += trade_profit

                    # Update total portfolio value
                    total_portfolio_value += trade_profit

                    transactions.append({
                        'Stock': script,
                        'Buy_Date': buy_date,
                        'Sell_Date': sell_date,
                        'Buy_Price': buy_price,
                        'Sell_Price': sell_price,
                        'Shares': shares_bought,
                        'Profit/Loss': trade_profit
                    })

                    holding = False  # Reset holding state

    # Final ROI Calculation
    portfolio_return_percentage = ((total_portfolio_value - Init_amt) / Init_amt) * 100

    # Print Summary
    print(f"Final Portfolio Value: {total_portfolio_value}")
    print(f"Total Profit/Loss: {total_portfolio_value - Init_amt}")
    print(f"Portfolio Return Percentage: {portfolio_return_percentage:.2f}%")

    return pd.DataFrame(transactions)

