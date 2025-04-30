import os

import boto3

from flask import Flask, jsonify, request

app = Flask(__name__)

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("MINIO_ENDPOINT"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    region_name="us-east-1",
)
BUCKET = "test-bucket"

# Garante que o bucket exista
try:
    buckets = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    if BUCKET not in buckets:
        s3.create_bucket(Bucket=BUCKET)
        print(f"Bucket '{BUCKET}' criado com sucesso.")
except Exception as e:
    print(f"Erro ao verificar/criar bucket: {e}")


@app.route("/")
def home():
    return "Flask + MinIO está rodando!"


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return "No file", 400
    s3.upload_fileobj(file, BUCKET, file.filename)
    return "Uploaded"


@app.route("/list")
def list_files():
    try:
        contents = s3.list_objects_v2(Bucket=BUCKET).get("Contents", [])
        keys = [obj["Key"] for obj in contents]
        if not keys:
            return jsonify(message="Bucket vazio")
        return jsonify(keys)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/minio-status")
def minio_status():
    try:
        names = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
        return jsonify(status="OK", buckets=names)
    except Exception as e:
        return jsonify(status="ERRO", error=str(e)), 500


@app.route("/upload-teste")
def upload_teste():
    try:
        s3.put_object(Bucket=BUCKET, Key="teste.txt", Body=b"Teste via endpoint")
        return "Teste enviado"
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
