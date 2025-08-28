# Cosmetology Clinic Chatbot

This repository contains a proof-of-concept chatbot for a cosmetology clinic.
It consists of a FastAPI `bot_api`, a Django-based `admin_panel`, and a
Qdrant vector database.

Secrets are delivered at runtime from **Yandex Lockbox**; no `.env` files are
stored in the repository.

## Deploy on Yandex Cloud VM
1. Create a Linux VM with access to Container Registry and Lockbox.
2. Install Docker and Docker Compose:
   ```bash
   sudo apt update && sudo apt install -y docker.io docker-compose-plugin
   ```
3. Clone the repository and start services:
   ```bash
   git clone <repo_url>
   cd botfocc/infra
   docker compose up -d --build
   ```

Services are available at:
- `http://localhost:8000` – FastAPI bot API
- `http://localhost:8001/admin/` – Django admin panel
- `http://localhost:6333` – Qdrant

## amoCRM webhook
Configure amoCRM to send chat webhooks to `https://<vm-ip>/amo/webhook` and set
the shared secret in Lockbox under `amo_secret`.

## Knowledge base import & reindex
Upload `.docx` or `.md` files via Django admin. After uploading, trigger
reindexing either from the admin action "Reindex" or via:
```bash
curl -X POST http://localhost:8000/kb/reindex
```
This ingests documents into Postgres and Qdrant for retrieval-augmented
generation.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE).
