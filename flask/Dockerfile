# Usa uma imagem base leve com Python
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários para dentro do container
COPY requirements.txt .
COPY main.py .

# Instala as dependências do Flask e boto3
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando para iniciar o app Flask
CMD ["python", "main.py"]
