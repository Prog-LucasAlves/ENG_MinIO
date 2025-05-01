import os
from functools import wraps

import boto3
from botocore.exceptions import ClientError

from flask import Flask, jsonify, request

app = Flask(__name__)

# Buckets padrão
DEFAULT_BUCKETS = ["gold", "silver", "bronze"]

# Variáveis de ambiente
API_TOKEN = os.getenv("API_TOKEN")  # padrão seguro para testes locais

# Cliente S3 (MinIO)
s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("MINIO_ENDPOINT"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    region_name="us-east-1",
)


# Middleware de autenticação
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token != f"Bearer {API_TOKEN}":
            return jsonify(error="Não autorizado"), 401
        return f(*args, **kwargs)

    return decorated


# Criar buckets padrão, se necessário
def ensure_buckets():
    try:
        existing = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
        for bucket in DEFAULT_BUCKETS:
            if bucket not in existing:
                s3.create_bucket(Bucket=bucket)
                print(f"Bucket '{bucket}' criado com sucesso.")
    except Exception as e:
        print(f"Erro ao verificar/criar buckets: {e}")


ensure_buckets()


@app.route("/")
def home():
    return "Flask + MinIO rodando com buckets padrão!"


@app.route("/upload/<bucket>", methods=["POST"])
def upload_file(bucket):
    if bucket not in DEFAULT_BUCKETS:
        return jsonify(error="Bucket inválido"), 400

    file = request.files.get("file")
    if not file:
        return jsonify(error="Arquivo não encontrado"), 400
    try:
        s3.upload_fileobj(file, bucket, file.filename)
        return f"Arquivo '{file.filename}' enviado para o bucket '{bucket}'"
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/list/<bucket>")
def list_files(bucket):
    if bucket not in DEFAULT_BUCKETS:
        return jsonify(error="Bucket inválido"), 400
    try:
        contents = s3.list_objects_v2(Bucket=bucket).get("Contents", [])
        if not contents:
            return jsonify(message="Bucket vazio")
        return jsonify([obj["Key"] for obj in contents])
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/bucket/<bucket_name>/empty", methods=["DELETE"])
@require_auth
def empty_bucket(bucket_name):
    if bucket_name not in DEFAULT_BUCKETS:
        return jsonify(error="Bucket inválido ou não autorizado"), 400
    try:
        contents = s3.list_objects_v2(Bucket=bucket_name).get("Contents", [])
        if not contents:
            return jsonify(message="Bucket já está vazio")

        objects_to_delete = [{"Key": obj["Key"]} for obj in contents]
        s3.delete_objects(Bucket=bucket_name, Delete={"Objects": objects_to_delete})
        return jsonify(
            message=f"Todos os arquivos do bucket '{bucket_name}' foram deletados."
        )
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/bucket/<bucket_name>", methods=["DELETE"])
@require_auth
def delete_bucket(bucket_name):
    if bucket_name not in DEFAULT_BUCKETS:
        return jsonify(error="Bucket inválido ou não autorizado"), 400
    try:
        contents = s3.list_objects_v2(Bucket=bucket_name).get("Contents", [])
        if contents:
            return jsonify(error="Bucket não está vazio"), 400
        s3.delete_bucket(Bucket=bucket_name)
        return jsonify(message=f"Bucket '{bucket_name}' deletado com sucesso")
    except ClientError as e:
        return jsonify(error=str(e)), 500


@app.route("/minio-status")
def minio_status():
    try:
        buckets = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
        return jsonify(status="OK", buckets=buckets)
    except Exception as e:
        return jsonify(status="ERRO", error=str(e)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
