from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# 📅 Configuration du DAG
default_args = {
    'owner': 'Jo',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
        dag_id='weather_etl_dag',
        default_args=default_args,
        description='ETL météo - Historique + Récent + Transform',
        start_date=datetime(2025, 7, 1),
        schedule_interval=None,  # On déclenche manuellement
        catchup=False
) as dag:

    extract_historical = BashOperator(
        task_id='extract_historical',
        bash_command='python3 /home/wesley/Documents/code/python/when-to-travel-Jo/Airflow/scripts/extract_historical.py'
    )

    extract_recent = BashOperator(
        task_id='extract_recent',
        bash_command='python3 /home/wesley/Documents/code/python/when-to-travel-Jo/Airflow/scripts/extract_recent.py'
    )

    transform = BashOperator(
        task_id='transform',
        bash_command='python3 /home/wesley/Documents/code/python/when-to-travel-Jo/Airflow/scripts/transform.py'
    )

    # 🔗 Dépendances : historique → récent → transform
    extract_historical >> extract_recent >> transform
