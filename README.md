# 🚀 MinIO no Render.com (Web Service Docker)

Este projeto executa o MinIO (armazenamento compatível com S3) como um **serviço web Docker** no Render.com, com acesso ao **console web pela URL pública**.

---

## 🧩 Como funciona

- Render só permite **uma porta pública** por Web Service
- Este setup inverte as portas do MinIO:
  - `9000` → Console Web (exposto publicamente)
  - `9001` → API S3 (acessível apenas internamente)
- Isso garante que você possa acessar o painel web do MinIO no navegador.

---

## 📦 Como usar

### 1. Suba este repositório no GitHub

```bash
git clone https://github.com/seu-usuario/minio-render.git
cd minio-render
