FROM quay.io/minio/minio

CMD ["server", "/data", "--address", ":9000", "--console-address", ":9001"]
