# Runbook

## VM setup
```
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
git clone <repo_url>
cd botfocc/infra
docker compose up -d --build
```

Services:
- bot_api: http://localhost:8000
- admin_panel: http://localhost:8001
- qdrant: http://localhost:6333
