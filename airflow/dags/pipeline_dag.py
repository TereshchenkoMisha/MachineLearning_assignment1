from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/opt/airflow/project"
DEPLOY_DIR  = f"{PROJECT_DIR}/code/deployment"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="spotify_genre_pipeline",
    description="Data engineering -> Model engineering -> Deployment",
    default_args=default_args,
    schedule_interval="*/10 * * * *",   # каждые 5 минут
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,                 # не запускать следующий прогон пока идёт текущий
    tags=["pml", "mlops"],
) as dag:

    preprocess_task = BashOperator(
        task_id="preprocess",
        bash_command=f"cd {PROJECT_DIR} && python code/datasets/preprocess.py",
    )

    train_task = BashOperator(
        task_id="train",
        bash_command=f"cd {PROJECT_DIR} && python code/models/train.py",
    )

    deploy_task = BashOperator(
    task_id="deploy",
    bash_command=(
        f"cd {DEPLOY_DIR} && "
        f"docker compose up -d --build --force-recreate api app"
        ),
    )

    preprocess_task >> train_task >> deploy_task