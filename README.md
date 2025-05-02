# 🚀 Flask + MinIO API

Este projeto é uma API REST desenvolvida com **Flask** para interagir com o **MinIO** (compatível com S3), oferecendo endpoints para upload, listagem, esvaziamento e exclusão de buckets com segurança.

---

## ✅ Recursos

- Conexão com MinIO via Boto3
- Buckets padrão: `gold`, `silver`, `bronze`
- Upload e listagem de arquivos por bucket
- Esvaziamento de bucket
- Exclusão de bucket (com validação)
- Autenticação por token para ações críticas
- Pronto para deploy no [Render](https://render.com)

---

## 📦 Endpoints

### Básicos

- `GET /` → Verifica se o serviço está online
- `GET /minio-status` → Retorna status do MinIO e buckets disponíveis

### Arquivos

- `POST /upload/<bucket>` → Upload de arquivo para um bucket
- `GET /list/<bucket>` → Lista arquivos de um bucket

### Buckets

- `DELETE /bucket/<bucket>/empty` → Esvazia o bucket (**requer autenticação**)
- `DELETE /bucket/<bucket>` → Remove o bucket se estiver vazio (**requer autenticação**)

---

## 🔐 Autenticação

As rotas de **esvaziar** e **deletar** bucket exigem um token JWT no header:

```http
Authorization: Bearer SEU_TOKEN_AQUI
```
