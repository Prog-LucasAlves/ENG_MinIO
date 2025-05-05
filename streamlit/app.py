import os

import boto3
from botocore.exceptions import ClientError

import streamlit as st

# Variáveis de ambiente do Render
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")


def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        region_name="us-east-1",
    )


st.title("🪣 Buckets no MinIO")

try:
    s3 = s3_client()
    buckets = s3.list_buckets().get("Buckets", [])
    if not buckets:
        st.warning("Nenhum bucket encontrado.")
    else:
        st.subheader("Buckets encontrados:")
        for bucket in buckets:
            st.markdown(f"- **{bucket['Name']}**")
except ClientError as e:
    st.error(f"Erro ao conectar: {e}")
