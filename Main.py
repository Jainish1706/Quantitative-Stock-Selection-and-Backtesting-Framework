if __name__ == "__main__":
    # Step 1: Select Stocks Based on Fundamental Analysis
    folder_path_1 = '/content/drive/MyDrive/Project_2_dataset'
    final_common_stocks = stock_selection(folder_path_1)

    # Step 2: Backtesting to Filter Stocks
    back_test_start_date = '2024-04-01'
    back_test_end_date = '2024-10-01'
    final_list = Backtesting(final_common_stocks, back_test_start_date, back_test_end_date)

    # Step 3: Monte Carlo Simulation for Optimal Weights
    monte_carlo_start_date = '2014-04-02'
    monte_carlo_end_date = '2024-03-31'
    optimized_weights = Monte_Carlo(final_list, monte_carlo_start_date, monte_carlo_end_date)

    # Step 4: Creating Dataset with Technical Indicators
    dataset_start_date = "2016-02-28"
    dataset_end_date = "2024-03-01"
    output_path = '/content/drive/MyDrive/nse_data'
    dataset_creation(final_list, dataset_start_date, dataset_end_date, output_path)

    # Step 5: Calculate Technical Indicators
    folder_path_2 = '/content/drive/MyDrive/nse_data'
    indicators_dataset(folder_path_2)

    # Step 6: Generate Buy/Sell Signals and Transactions
    scripts = [stock.split('.')[0] for stock in final_list]  # Remove ".NS"
    result_dfs = {}  # Dictionary to store result_df for each stock

    for script in scripts:
        daily_data = pd.read_csv(f'/content/drive/MyDrive/nse_data/Daily/{script}_Daily.csv')

        # Generate Buy/Sell signals
        buy, sell = calculate_buy_sell_tags(daily_data)
        buy_df = pd.DataFrame(buy, columns=['Date', 'Buy_Tag'])
        sell_df = pd.DataFrame(sell, columns=['Date', 'Sell_Tag'])
        result_df = pd.merge(buy_df, sell_df, on='Date')

        # Store result_df for use in closed_loop()
        result_dfs[script] = result_df

        # Generate transactions for review
        transaction = generate_transactions(daily_data, result_df, script)

    # Step 7: Run Closed Loop Strategy
    Init_amt = 1000000  # Example: Initial capital of 1,000,000
    transactions_df = closed_loop(Init_amt, optimized_weights, final_list, folder_path_2, result_dfs)

    # Step 8: Save the Final Transactions to CSV for Review
    print(transactions_df)
    print("\nClosed-loop strategy execution completed. Results saved to CSV.")
