import requests
import os
import argparse
from datetime import datetime

NEWS_API_KEY = os.getenv("NEWS_API_KEY") 

# ----------------------------------------------------------------------------------------------------- #

def fetch_news(query, from_date, to_date, language="en"):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "sortBy": "relevancy",
        "language": language,
        "apiKey": NEWS_API_KEY,
        "pageSize": 100
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "ok":
        print("[!] Erro na NewsAPI:", data)
        return []

    return data["articles"]

# ----------------------------------------------------------------------------------------------------- #

def save_news(articles, company, output_dir="data/raw"):
    os.makedirs(output_dir, exist_ok=True)
    today = datetime.today().strftime("%Y%m%d")
    filename = f"news_{company.lower()}_{today}.json"
    path = os.path.join(output_dir, filename)

    import json
    with open(path, "w") as f:
        json.dump(articles, f, indent=4)

    print(f"[✓] Notícias guardadas em {path}")
    return path

# ----------------------------------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", type=str, required=True, help="Empresa para pesquisa (ex: Apple)")
    parser.add_argument("--from_date", type=str, required=True, help="Data inicial (YYYY-MM-DD)")
    parser.add_argument("--to_date", type=str, required=True, help="Data final (YYYY-MM-DD)")

    args = parser.parse_args()

    articles = fetch_news(args.company, args.from_date, args.to_date)
    if articles:
        save_news(articles, args.company)

if __name__ == "__main__":
    main()
