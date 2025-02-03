def Backtesting(final_common_stocks, start_date, end_date):
  stocks = final_common_stocks['Stock'].to_list()
  temp = []
  for symbol in stocks:
    temp.append(symbol+".NS")
  stocks = temp

  # start_date '2024-04-01'
  # end_date = '2024-10-01'
  index_symbol = '^CNX100'

  stock_data = yf.download(stocks, start=start_date, end=end_date)
  stock_adj_close = stock_data['Close']

  # Download index data
  index_data = yf.download(index_symbol, start=start_date, end=end_date)
  index_adj_close = index_data['Close']

  # Instead of using specific dates, get the first and last dates from the index
  selected_dates = [stock_adj_close.index[0], stock_adj_close.index[-1]]
  stock_prices = stock_adj_close.loc[selected_dates]
  index_prices = index_adj_close.loc[selected_dates]

  #Calculating return for stocks and index
  stock_prices = stock_prices.T
  index_prices = index_prices.T
  stock_prices['returns'] = (stock_prices['2024-09-30'] - stock_prices['2024-04-01'])/stock_prices['2024-04-01']*100
  index_return = (index_prices['2024-09-30']-index_prices['2024-04-01'])/index_prices['2024-04-01']*100
  index_return_value = index_return.iloc[0]

  # Filter stocks whose return is 5% greater than the index return
  selected_stocks = stock_prices[stock_prices['returns'] > index_return_value + 5*0.5]

  # Print filtered stocks
  print("\nStocks with annualized return greater than 5% index return:")
  # print(selected_stocks)

  final_list = selected_stocks.index.to_list()
  final_list_df = pd.DataFrame(final_list, columns=['Stocks'])
  return final_list