# 🚀 MinIO no Render.com

Este projeto contém a configuração necessária para executar uma instância do [MinIO](https://min.io/) — um serviço de armazenamento compatível com S3 — como um serviço web permanente no [Render.com](https://render.com), usando Docker e Deploy via Blueprint (`render.yaml`).

---

## 📦 O que está incluído

- `Dockerfile`: Usa a imagem oficial do MinIO
- `render.yaml`: Define o serviço no Render com variáveis de ambiente
- Suporte a:
  - Console Web (porta `9001`)
  - API S3 (porta `9000`)

---

## 🔧 Pré-requisitos

- Conta no [Render.com](https://render.com)
- Conta no [GitHub](https://github.com)
- Git instalado localmente

---

## 🚀 Como fazer o deploy

### 1. Clone este repositório ou crie o seu

```bash
git clone https://github.com/seu-usuario/minio-render.git
cd minio-render
