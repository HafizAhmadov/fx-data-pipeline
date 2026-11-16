from datetime import timedelta

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

PROJECT = "/Users/thescientist/Developer/fx-data-pipeline"
PYTHON = f"{PROJECT}/.venv/bin/python"
DBT = f"{PROJECT}/.venv/bin/dbt"

default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="fx_pipeline",
    description="Load CBAR exchange rates, check freshness, build dbt models",
    schedule="17 6 * * 1-5",
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=["fx", "cbar"],
) as dag:

    extract_load = BashOperator(
        task_id="extract_load",
        bash_command=f"cd {PROJECT} && {PYTHON} src/backfill.py",
    )

    source_freshness = BashOperator(
        task_id="source_freshness",
        bash_command=f"cd {PROJECT}/dbt && {DBT} source freshness",
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=f"cd {PROJECT}/dbt && {DBT} build",
    )

    extract_load >> source_freshness >> dbt_build