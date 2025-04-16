import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta
import argparse

# ----------------------------------------------------------------------------------------------------- #

def fetch_stock_data(ticker: str, start: str = None, end: str = None, days: int = None) -> pd.DataFrame:
    if days:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days)
    else:
        end_date = datetime.strptime(end, "%Y-%m-%d") if end else datetime.today()
        start_date = datetime.strptime(start, "%Y-%m-%d") if start else end_date - timedelta(days=180)

    df = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
    return df

# ----------------------------------------------------------------------------------------------------- #

def save_to_csv(df, ticker, folder="data/raw"):
    os.makedirs(folder, exist_ok=True)
    filename = f"{ticker.lower()}_20250416.csv"
    filepath = os.path.join(folder, filename)
    
    df.to_csv(filepath, index=False)
    
    print(f"[✓] Data saved in: {filepath}")
    return filepath

# ----------------------------------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(description="Fetch stock data from Yahoo Finance")
    parser.add_argument("--ticker", type=str, required=True, help="Stock ticker (e.g., AAPL, TSLA)")
    parser.add_argument("--start", type=str, help="Start date (format YYYY-MM-DD)")
    parser.add_argument("--end", type=str, help="End date (format YYYY-MM-DD)")
    parser.add_argument("--days", type=int, help="Number of most recent days (overrides start/end)")

    args = parser.parse_args()

    df = fetch_stock_data(args.ticker, args.start, args.end, args.days)
    
    if df.empty:
        print("[!] No data found for this range.")
    else:
        save_to_csv(df, args.ticker)


if __name__ == "__main__":
    main()