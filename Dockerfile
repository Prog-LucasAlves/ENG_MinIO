FROM quay.io/minio/minio

CMD ["server", "/data", "--address", ":9001", "--console-address", ":9000"]
