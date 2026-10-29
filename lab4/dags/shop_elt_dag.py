"""KedaiKita ELT pipeline: extract -> load -> dbt run -> dbt test -> report."""
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

LAB = "/home/codespace/workshop/lab4"
TOOLS = "/home/codespace/venvs/dbt/bin"  # Python, dbt and DuckDB live here

with DAG(
    dag_id="shop_elt_pipeline",
    description="Daily ELT for the KedaiKita online shop",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",  # run once a day
    catchup=False,  # don't run for all the past days
    tags=["workshop", "lab4"],
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command=f"cd {LAB} && {TOOLS}/python scripts/extract.py",
    )

    load = BashOperator(
        task_id="load_raw",
        bash_command=f"cd {LAB} && {TOOLS}/python scripts/load_raw.py",
    )

    transform = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {LAB}/shop_dbt && {TOOLS}/dbt run --profiles-dir .",
    )

    test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {LAB}/shop_dbt && {TOOLS}/dbt test --profiles-dir .",
    )

    report = BashOperator(
        task_id="report",
        bash_command=f"cd {LAB} && {TOOLS}/python scripts/show_report.py",
    )

    # The order to run the tasks in
    extract >> load >> transform >> test >> report
