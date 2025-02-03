def dataset_creation(final_list, start_date, end_date, output_path):
  # Define your NSE tickers and dates
  nse_tickers = final_list
  # start_date = "2016-02-28"
  # end_date = "2024-03-01"

  # Define the intervals
  intervals = {
      "Daily": "1d",
      "Weekly": "1wk",
      "Monthly": "1mo"
  }

  # Set output directory path to Google Drive
  output_dir = output_path   #'/content/drive/MyDrive/nse_data'
  os.makedirs(output_dir, exist_ok=True)

  # Download data for each ticker and each interval
  for ticker in nse_tickers:
      for interval_name, interval in intervals.items():
          try:
              # Download historical data with specific interval
              data = yf.download(ticker, start=start_date, end=end_date, interval=interval)

              # Reorder columns and reset index to make Date a column
              if not data.empty:
                  data.reset_index(inplace=True)  # Convert Date index into a column
                  data = data[['Date', 'Close', 'High', 'Low', 'Open', 'Volume']]  # Ensure correct order

                  # Save to CSV with Date as a column
                  sub_dir = os.path.join(output_dir, interval_name)
                  os.makedirs(sub_dir, exist_ok=True)
                  csv_file = os.path.join(sub_dir, f"{ticker.replace('.NS', '')}_{interval_name}.csv")
                  data.to_csv(csv_file, index=False, header=True)  # Do not save index

                  print(f"Saved {interval_name} data for {ticker} to {csv_file}")
              else:
                  print(f"No {interval_name} data found for {ticker}")
          except Exception as e:
              print(f"Error downloading {interval_name} data for {ticker}: {e}")


def indicators_dataset(folder_path):
  def read_csv(file_path):
      df = pd.read_csv(file_path)
      df['Date'] = pd.to_datetime(df['Date'])
      return df

  def calculate_monthly_indicators(df):
      df['SMA_20'] = ta.sma(df['Close'], timeperiod=20)
      df['Choppiness_Index'] = ta.adx(df['High'], df['Low'], df['Close'], timeperiod=14)['ADX_14']
      ST = ta.atr(df["High"], df["Low"], df["Close"], timeperiod=14)  # Example for SuperTrend (adjust as needed)
      df["SuperTrend"] = ST
      return df[['Date', 'Open', 'Close', 'High','Volume', 'SMA_20', 'Choppiness_Index', 'SuperTrend']]

  def calculate_weekly_indicators(df):
      macd_result = ta.macd(df["Close"], fastperiod=12, slowperiod=26, signalperiod=9)
      df["MACD"] = macd_result["MACD_12_26_9"]
      df["MACD_Signal"] = macd_result["MACDs_12_26_9"]
      df['RSI'] = ta.rsi(df['Close'], timeperiod=14)
      df['SMA_50'] = ta.sma(df['Close'], timeperiod=50)
      df['EMA_20'] = ta.ema(df['Close'], timeperiod=20)
      df['EMA_10'] = ta.ema(df['Close'], timeperiod=10)
      return df[['Date','Open', 'Close','High', 'MACD', 'MACD_Signal', 'RSI', 'SMA_50', 'EMA_20', 'EMA_10']]

  def calculate_daily_indicators(df):
      df['VWSMA_200'] = df['Close'].rolling(window=200).mean()
      df['VWEMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
      df['VWEMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
      df['RSI_Daily'] = ta.rsi(df['Close'], timeperiod=14)
      adx_indicators = ta.adx(df['High'], df['Low'], df['Close'], timeperiod=14)
      df['ADX'] = adx_indicators['ADX_14']
      return df[['Date','Open', 'Close', 'High', 'Low','VWSMA_200', 'VWEMA_50', 'VWEMA_20', 'RSI_Daily', 'ADX']]

  def main():
      # Specify the base directory containing stock data
      stock_data_folder = folder_path #"/content/drive/MyDrive/nse_data"  # Replace with actual path
      subfolders = ["Daily", "Weekly", "Monthly"]

      for subfolder in subfolders:
          subfolder_path = os.path.join(stock_data_folder, subfolder)
          for file in os.listdir(subfolder_path):
              if file.endswith('.csv'):
                  file_path = os.path.join(subfolder_path, file)
                  df = pd.read_csv(file_path, skiprows = [1])
                  df['Date'] = pd.to_datetime(df['Date'])

                  interval_name = file.split('_')[1].split('.')[0]
                  stock_name = file.split('_')[0]

                  # Apply relevant indicator calculations
                  if interval_name == 'Daily':
                      indicators_df = calculate_daily_indicators(df)
                      indicators_df = indicators_df.dropna()
                  elif interval_name == 'Weekly':
                      indicators_df = calculate_weekly_indicators(df)
                      indicators_df = indicators_df.dropna()
                  else:  # Monthly
                      indicators_df = calculate_monthly_indicators(df)
                      indicators_df = indicators_df.dropna()


                  output_file_path = os.path.join(subfolder_path, f"{stock_name}_{interval_name}.csv")
                  indicators_df.to_csv(output_file_path, index=False)
                  print(f"Saved indicators to {output_file_path}")

  main()