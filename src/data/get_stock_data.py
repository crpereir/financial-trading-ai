import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta
import argparse


def fetch_stock_data(ticker: str, start: str = None, end: str = None, days: int = None) -> pd.DataFrame:
    if days:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days)
    else:
        end_date = datetime.strptime(end, "%Y-%m-%d") if end else datetime.today()
        start_date = datetime.strptime(start, "%Y-%m-%d") if start else end_date - timedelta(days=180)

    df = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
    return df


def save_to_csv(df: pd.DataFrame, ticker: str, output_dir: str = "data/raw") -> str:
    os.makedirs(output_dir, exist_ok=True)
    today = datetime.today().strftime("%Y%m%d")
    filename = f"{ticker.lower()}_{today}.csv"
    path = os.path.join(output_dir, filename)
    df.to_csv(path)
    print(f"[✓] Dados guardados em: {path}")
    return path


def main():
    parser = argparse.ArgumentParser(description="Fetch stock data from Yahoo Finance")
    parser.add_argument("--ticker", type=str, required=True, help="Ticker da ação (ex: AAPL, TSLA)")
    parser.add_argument("--start", type=str, help="Data de início (formato YYYY-MM-DD)")
    parser.add_argument("--end", type=str, help="Data de fim (formato YYYY-MM-DD)")
    parser.add_argument("--days", type=int, help="Número de dias mais recentes (ignora start/end)")

    args = parser.parse_args()

    df = fetch_stock_data(args.ticker, args.start, args.end, args.days)
    
    if df.empty:
        print("[!] Nenhum dado encontrado para esse intervalo.")
    else:
        save_to_csv(df, args.ticker)


if __name__ == "__main__":
    main()
