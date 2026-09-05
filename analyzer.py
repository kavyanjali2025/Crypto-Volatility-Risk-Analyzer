import yfinance as yf 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Download Bitcoin data
data = yf.download(
    "BTC-USD",       
    start="2024-01-01",
    end="2026-01-01"
)

print(data.head()) 

# Calculate daily returns
data['Returns'] = data['Close'].pct_change() 

# Calculate rolling volatility (standard deviation of returns)
data['Volatility'] = data['Returns'].rolling(window=30).std() * np.sqrt(30)

# Visualize Bitcoin Price

plt.figure(figsize=(12, 6))

plt.plot(data.index, data["Close"])

plt.title("Bitcoin Price")
plt.xlabel("Date")
plt.ylabel("Closing Price (USD)")

plt.grid(True)
plt.show()

# Visualize Volatility
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Volatility'])
plt.title('Bitcoin Volatility (30-day Rolling)')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.show()

# Cumulative Return
data["Cumulative_Return"] = (1 + data["Returns"]).cumprod() - 1

# Get Close as a single Series
close = data["Close"].squeeze()

# Highest closing price seen so far
data["Running_Max"] = close.cummax()

# Drawdown from the previous peak
data["Drawdown"] = (
    close - data["Running_Max"]
) / data["Running_Max"]

# Maximum Drawdown
max_drawdown = data["Drawdown"].min()

print("Maximum Drawdown:", max_drawdown)

# Calculate average daily return
average_return = data["Returns"].mean()

print("Average Daily Return:", average_return)

# Calculate Sharpe Ratio
sharpe_ratio = (
    data["Returns"].mean() / data["Returns"].std()
) * np.sqrt(365)

print("Sharpe Ratio:", sharpe_ratio)

# Calculate 95% Value at Risk
VaR_95 = data["Returns"].quantile(0.05)

print("95% Value at Risk:", VaR_95)

# Visualize Cumulative Return
plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Cumulative_Return"])
plt.title("Cumulative Return")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.show()


# Visualize Drawdown
plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Drawdown"])
plt.title("Bitcoin Drawdown")
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.show()


# Visualize Sharpe Ratio
plt.figure(figsize=(8, 5))

plt.barh(["Bitcoin"], [sharpe_ratio])

plt.axvline(0, linestyle="--")
plt.axvline(1, linestyle="--", label="Sharpe = 1")

plt.title("Bitcoin Sharpe Ratio")
plt.xlabel("Sharpe Ratio")
plt.legend()

plt.show()


# Visualize VaR
plt.figure(figsize=(10, 6))

plt.hist(
    data["Returns"].dropna(),
    bins=50
)

plt.axvline(
    VaR_95,
    linestyle="--",
    label=f"95% VaR = {VaR_95:.2%}"
)

plt.title("Bitcoin Daily Returns and 95% VaR")
plt.xlabel("Daily Return")
plt.ylabel("Frequency")
plt.legend()

plt.show()