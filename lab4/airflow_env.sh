# Airflow settings for Lab 4. Load them into a terminal with:  source airflow_env.sh
export AIRFLOW_HOME=/home/codespace/airflow
export AIRFLOW__CORE__DAGS_FOLDER=/home/codespace/workshop/lab4/dags
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL=30
export AIRFLOW__WEBSERVER__ENABLE_PROXY_FIX=True
export PATH=/home/codespace/venvs/airflow/bin:$PATH
echo "Airflow settings loaded. AIRFLOW_HOME=$AIRFLOW_HOME"
