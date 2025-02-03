def stock_selection(folder_path):
  parent_folder_path = folder_path 
  
  # Initialize a dictionary to hold results for each sector
  sector_dataframes = {}

  # List to store common stocks across all sectors
  all_common_stocks = []

  # Walk through subfolders
  for root, dirs, files in os.walk(parent_folder_path):
      if root == parent_folder_path:
          continue  # Skip the parent folder itself

      sector = os.path.basename(root)  # Extract sector name from folder name
      sector_means = []  # List to store mean results for the sector

      for file_name in files:
          if file_name.endswith('.xlsx'):  # Only process Excel files
              file_path = os.path.join(root, file_name)
              # print(f"Processing file: {file_path}")

              # Read and clean the Excel file
              data = pd.read_excel(file_path, sheet_name='Ratio_Analysis', skiprows=3)
              data = data.dropna(axis=1, how='all')  # Drop columns with all NaN values
              data.rename(
                  columns=lambda x: pd.to_datetime(x, errors='coerce').strftime('%Y-%m-%d')
                  if pd.to_datetime(x, errors='coerce') is not pd.NaT else x, inplace=True
              )

              # Transpose and clean data
              data_transposed = data.T
              data_transposed = data_transposed.fillna(0)
              data_transposed.columns = data_transposed.iloc[0]
              data_transposed = data_transposed[1:]
              data_transposed = data_transposed.drop(columns='Price', errors='ignore')

              # Split data into high and low indicators
              data_transposed_high = data_transposed[['EBITDA Margin', 'PAT Margin', 'ROE', 'ROCE']]
              data_transposed_low = data_transposed[['PE', 'PEG', 'D/E', 'P/B']]

              # Normalize and apply PCA
              scaler = StandardScaler()
              data_normalized_high = scaler.fit_transform(data_transposed_high)
              data_normalized_low = scaler.fit_transform(data_transposed_low)

              pca = PCA(n_components=1)
              pca_result_high = pca.fit_transform(data_normalized_high)
              pca_result_low = pca.fit_transform(data_normalized_low)

              # Calculate mean
              mean_high = pca_result_high.mean()
              mean_low = pca_result_low.mean()

              # Append to sector_means
              sector_means.append({
                  "Stock": os.path.splitext(file_name)[0],  # Stock name from file name
                  "Mean_High": mean_high,
                  "Mean_Low": mean_low
              })

      # Convert sector_means to DataFrame
      sector_df = pd.DataFrame(sector_means)
      sector_dataframes[sector] = sector_df  # Store in dictionary

      if not sector_df.empty:
          # Get sorted DataFrames
          sector_df1 = sector_df[['Stock', 'Mean_High']].sort_values(by='Mean_High', ascending=False)
          sector_df2 = sector_df[['Stock', 'Mean_Low']].sort_values(by='Mean_Low')

          n = len(sector_df1)
          m = len(sector_df2)
          reqd = n//2 if n % 2 == 0 else (n+1)//2

          # Get the first 50 percent rows of each DataFrame
          top_n_high = set(sector_df1.head(reqd)['Stock'])
          top_n_low = set(sector_df2.head(reqd)['Stock'])

          # Find common stocks
          common_stocks = top_n_high.intersection(top_n_low)

          # Filter the sector_df for common stocks
          common_stocks_df = sector_df[sector_df['Stock'].isin(common_stocks)].copy()
          common_stocks_df['Sector'] = sector  # Add sector column

          # Append to the list
          all_common_stocks.append(common_stocks_df)


  # Combine all sector common stocks into one DataFrame
  final_common_stocks_df = pd.concat(all_common_stocks, ignore_index=True)


  final_common_stocks_df_high = final_common_stocks_df[["Stock", "Mean_High", "Sector"]].sort_values(by='Mean_High', ascending=False)
  final_common_stocks_df_low = final_common_stocks_df[["Stock", "Mean_Low", "Sector"]].sort_values(by='Mean_Low')


  # Find common stocks between high and low DataFrames
  common_stocks_final = set(final_common_stocks_df_high['Stock']).intersection(final_common_stocks_df_low['Stock'])

  # Filter the original DataFrame for these common stocks
  final_common_stocks = final_common_stocks_df[final_common_stocks_df['Stock'].isin(common_stocks_final)]

  # Calculate the number of common stocks
  num_common_stocks = len(final_common_stocks)

  # If the count exceeds 30, limit it to 30 stocks
  if num_common_stocks > 30:
      final_common_stocks = final_common_stocks.head(30)

  return final_common_stocks
