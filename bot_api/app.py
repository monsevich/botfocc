"""FastAPI entrypoint for bot API."""
from fastapi import FastAPI, HTTPException, Request
from .settings import load_settings
from .security import validate_signature
from .amocrm_client import parse_incoming, send_reply
from .rag.ingest import reindex_kb
from .logic.orchestrator import handle_intent
from .db import pg

app = FastAPI()
settings = None

@app.on_event("startup")
async def startup():
    global settings
    settings = load_settings()
    pg.settings = settings
    # Инициализируем пул PG (создастся при первом вызове)
    await pg.get_pool(settings.database_dsn)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/amo/webhook")
async def amo_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Signature", "")
    if not validate_signature(body, signature, settings.amo_secret):
        raise HTTPException(status_code=403, detail="invalid signature")
    payload = await request.json()
    chat_id, text = parse_incoming(payload)
    await handle_intent(chat_id, text)
    return {"status": "accepted"}

@app.post("/kb/reindex")
async def kb_reindex():
    await reindex_kb()
    return {"status": "queued"}
