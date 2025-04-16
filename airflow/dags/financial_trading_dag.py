# airflow/dags/financial_trading_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.data.get_stock import download_stock_data
from src.data.get_news import download_news
from src.nlp.sentiment_analysis import analyze_news_sentiment, save_sentiment
from src.ml.train_model import train
from src.vis.plot_sentiment import plot_sentiment

# Função para o Airflow executar
def download_stock_data_task(**kwargs):
    download_stock_data(ticker="AAPL", start="2023-10-01", end="2024-04-01")

def download_news_task(**kwargs):
    download_news(company="Apple", from_date="2023-10-01", to_date="2024-04-01")

def analyze_sentiment_task(**kwargs):
    input_path = "data/raw/news_apple_20240401.json"
    df = analyze_news_sentiment(input_path)
    save_sentiment(df, "apple")

def train_model_task(**kwargs):
    train()

def plot_sentiment_task(**kwargs):
    plot_sentiment()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 16),  
    'retries': 1,
}

dag = DAG(
    'financial_trading_dag',
    default_args=default_args,
    description='DAG para orquestrar o projeto de trading',
    schedule_interval=None,  
)

task1 = PythonOperator(
    task_id='download_stock_data',
    python_callable=download_stock_data_task,
    dag=dag,
)

task2 = PythonOperator(
    task_id='download_news',
    python_callable=download_news_task,
    dag=dag,
)

task3 = PythonOperator(
    task_id='analyze_sentiment',
    python_callable=analyze_sentiment_task,
    dag=dag,
)

task4 = PythonOperator(
    task_id='train_model',
    python_callable=train_model_task,
    dag=dag,
)

task5 = PythonOperator(
    task_id='plot_sentiment',
    python_callable=plot_sentiment_task,
    dag=dag,
)

task1 >> task2 >> task3 >> task4 >> task5
