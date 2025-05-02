#!/bin/bash
set -e

# Inicializa o banco de dados se não estiver pronto
airflow db check || airflow db init

# Cria o usuário admin (apenas se não existir)
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin || true

# Inicia o webserver
exec airflow webserver
