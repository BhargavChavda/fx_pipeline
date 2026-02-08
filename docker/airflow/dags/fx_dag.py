from airflow import DAG 
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime, timezone
import os

with DAG(
        dag_id="fx_pipeline",
        start_date=datetime(2025,2,6, tzinfo=timezone.utc),
        schedule_interval = '@daily',
        catchup=False,
        tags=["fx_pipeline"],
        ) as dag:
        run_pipeline=DockerOperator(
                task_id="run_fx_pipeline",
                image = "fx_pipeline:latest",
                docker_url = "unix://var/run/docker.sock",
                network_mode = "bridge",
                environment={
                    "CURRENCYFREAKS_API_KEY": os.environ.get("CURRENCYFREAKS_API_KEY"),
                    "DB_HOST": "host.docker.internal",
                    "DB_PORT": "5432",
                    "DB_NAME": "etl_db",
                    "DB_USER": "bha",
                },
                mounts=[
                    Mount(source="/Users/lydia/Dev/Data_Engineering/fx_pipeline/data/raw", target="/data/raw", type="bind"),
                    Mount(source="/Users/lydia/Dev/Data_Engineering/fx_pipeline/data/processed", target="/data/processed", type="bind"),
                ],
                auto_remove=True,
                mount_tmp_dir=False,
                tty=True,
            )
