import os
from datetime import datetime

import boto3
from airflow.operators.python import PythonOperator

from airflow import DAG


def listar_arquivos_do_bucket():
    s3 = boto3.client(
        "s3",
        endpoint_url=os.getenv("MINIO_ENDPOINT"),
        aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
        region_name="us-east-1",
    )

    bucket = "gold"  # ou "silver", "bronze"
    print(f"🔍 Listando arquivos no bucket '{bucket}'...")

    try:
        response = s3.list_objects_v2(Bucket=bucket)
        contents = response.get("Contents", [])
        if not contents:
            print(f"📂 O bucket '{bucket}' está vazio.")
        else:
            for obj in contents:
                print(f"📄 {obj['Key']}")
    except Exception as e:
        print(f"❌ Erro ao acessar bucket: {e}")


default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id="minio_listar_arquivos",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["minio", "s3", "exemplo"],
) as dag:

    tarefa_listar = PythonOperator(
        task_id="listar_arquivos",
        python_callable=listar_arquivos_do_bucket,
    )
