#!/bin/bash

# Inicializa o banco de dados
airflow db init

# Cria o usuário admin (somente na primeira vez)
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin || true

# Inicia o scheduler em background
airflow scheduler &

# Inicia o webserver (porta 8080)
exec airflow webserver
