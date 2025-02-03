# Quantitative Stock Selection and Trading Strategy

## Overview
This project implements a **quantitative stock selection and trading strategy** using **fundamental analysis, backtesting, Monte Carlo simulations, and technical indicators**. The code is designed to select stocks, optimize portfolio weights, and implement a **closed-loop trading strategy** based on buy/sell signals.

## Features
- **Stock Selection:** Selects stocks using **fundamental analysis** (EBITDA margin, ROE, PE ratio, etc.).
- **Backtesting:** Filters stocks based on their historical performance.
- **Monte Carlo Simulation:** Optimizes portfolio weights for maximum Sharpe ratio.
- **Technical Indicators:** Calculates **SMA, RSI, MACD, ATR, ADX**, and other indicators.
- **Trading Strategy:** Implements a **rule-based strategy** for buy/sell decisions.
- **Performance Evaluation:** Computes portfolio returns and evaluates profitability.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Install Dependencies
Ensure you have **Python 3.8+** installed, then install required packages:
```bash
pip install -r requirements.txt
```
> **Note:** The script uses **Yahoo Finance (yfinance)** for fetching stock data.

---

## Usage

### 1. Run the Main Script
The script is structured into multiple functions. To execute the entire workflow:
```bash
python Quant_Stock_Selection_trading.py
```

### 2. Stock Selection
Modify `folder_path_1` in `main()` to point to your dataset directory:
```python
folder_path_1 = "/path/to/your/dataset"
final_common_stocks = stock_selection(folder_path_1)
```

### 3. Backtesting
Set the **backtesting period** and filter stocks:
```python
final_list = Backtesting(final_common_stocks, start_date="2024-04-01", end_date="2024-10-01")
```

### 4. Portfolio Optimization
Run **Monte Carlo simulation** to find optimal weights:
```python
optimized_weights = Monte_Carlo(final_list, start_date="2014-04-02", end_date="2024-03-31")
```

### 5. Trading Strategy Execution
Execute the **closed-loop trading strategy**:
```python
transactions_df = closed_loop(Init_amt=1000000, Weights=optimized_weights, stock_list=final_list, folder_path=folder_path_2, result_dfs=result_dfs)
```
The output will contain **buy/sell transactions, profit/loss, and portfolio return percentage**.

---

## Directory Structure
```
/your-repo
│── Quant_Stock_Selection_trading.py   # Main script
│── requirements.txt                   # Python dependencies
│── data/                               # Folder for stock data (optional)
│── results/                            # Output folder for results
```

---

## Dependencies
- `pandas`
- `numpy`
- `yfinance`
- `sklearn`
- `matplotlib`
- `pandas_ta`

Install all dependencies using:
```bash
pip install -r requirements.txt
```

---

## Contributions
Feel free to fork this repository and submit **pull requests** if you have improvements.

---

## License
This project is **open-source** and available under the **MIT License**.
