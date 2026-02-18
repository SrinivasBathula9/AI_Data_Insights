import yfinance as yf
ticker = yf.Ticker("AAPL")
print(f"Info: {ticker.info.get('longName')}")
