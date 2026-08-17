"""
Stock Price Analyzer
----------------------
No trading strategy here - just pulling real stock data and 
calculating basic numbers that matter in finance.

Install: pip install yfinance pandas matplotlib
Run:     python stock_analyzer.py
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# STEP 1: Download stock price history
# ---------------------------------------------------------
TICKER = "RELIANCE.NS"   # try "TCS.NS", "INFY.NS", "TATASTEEL.NS" too
data = yf.download(TICKER, start="2023-01-01", end="2024-01-01")
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)
data = data[["Close"]].dropna()

# ---------------------------------------------------------
# STEP 2: Daily Return
# ---------------------------------------------------------
# "How much did the price change from yesterday to today, in %"
# Example: price went 100 -> 102, that's a +2% daily return
data["Daily_Return_%"] = data["Close"].pct_change() * 100

# ---------------------------------------------------------
# STEP 3: Key stats everyone in finance looks at
# ---------------------------------------------------------
avg_daily_return = float(data["Daily_Return_%"].mean())
volatility = float(data["Daily_Return_%"].std())
max_price = float(data["Close"].max())
min_price = float(data["Close"].min())
total_return = float((data["Close"].iloc[-1] / data["Close"].iloc[0] - 1) * 100)

best_day = data["Daily_Return_%"].idxmax()
worst_day = data["Daily_Return_%"].idxmin()

# ---------------------------------------------------------
# STEP 4: Print a simple report
# ---------------------------------------------------------
print(f"\n--- {TICKER} Analysis (2023) ---")
print(f"Total Return over the year : {total_return:.2f}%")
print(f"Average Daily Return       : {avg_daily_return:.3f}%")
print(f"Volatility (Std Dev)       : {volatility:.3f}%")
print(f"Highest Price               : Rs {max_price:.2f}")
print(f"Lowest Price                : Rs {min_price:.2f}")
print(f"Best single day             : {best_day.date()} ({data['Daily_Return_%'].max():.2f}%)")
print(f"Worst single day            : {worst_day.date()} ({data['Daily_Return_%'].min():.2f}%)")

# ---------------------------------------------------------
# STEP 5: Plot the price over the year
# ---------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(data["Close"])
plt.title(f"{TICKER} - Closing Price (2023)")
plt.xlabel("Date")
plt.ylabel("Price (Rs)")
plt.savefig("price_chart.png")
plt.show()
