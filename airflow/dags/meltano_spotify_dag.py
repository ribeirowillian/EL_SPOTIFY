from datetime import datetime
from airflow.providers.docker.operators.docker import DockerOperator
from airflow import DAG
from airflow.models import Variable

default_args = {
    "trigger_rule": "all_done",
    "email_on_failure": True,
    "email_on_retry": False,
    "pool": "meltano_pool",
    "concurrency": 4,
    "retries": 2
}

def meltano_task(task_id, dag):
    return DockerOperator(
        task_id=task_id,
        image='meltano',
        auto_remove=True,
        network_mode='host',
        entrypoint=[
        "/bin/bash",
        "-c",
        f'''
        meltano config tap-spotify set client_id "{Variable.get('CLIENT_ID')}" &&
        meltano config tap-spotify set client_secret "{Variable.get('CLIENT_SECRET')}" &&
        meltano config tap-spotify set refresh_token "{Variable.get('REFRESH_TOKEN')}" &&
        meltano config target-snowflake set password  "{Variable.get('TARGET_SNOWFLAKE_PASSWORD')}" &&
        meltano run tap-spotify target-snowflake
        '''
        ],
        dag=dag
    )

with DAG(
    dag_id='spotify_extract_dag',
    default_args=default_args,
    description='DAG to run Spotify extraction pipeline',
    schedule_interval="0 0 * * *",  # Scheduled daily at midnight
    start_date=datetime(2024, 4, 19),
    tags=["EL", "SPOTIFY", "PROD"],
    catchup=False
) as dag:
    el_spotify = meltano_task(
        task_id="el_spotify",
        dag=dag
    )
