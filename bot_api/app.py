"""FastAPI entrypoint for bot API."""
from fastapi import FastAPI, HTTPException, Request

from .settings import Settings
from .security import validate_signature
from .amocrm_client import parse_incoming, send_reply
from .rag.ingest import reindex_kb
from .logic.orchestrator import handle_intent

app = FastAPI()
settings = Settings()


@app.get("/health")
async def health() -> dict[str, str]:
    """Basic healthcheck."""
    return {"status": "ok"}


@app.post("/amo/webhook")
async def amo_webhook(request: Request) -> dict[str, str]:
    """Receive amoCRM webhook with signature validation."""
    body = await request.body()
    signature = request.headers.get("X-Signature", "")
    if not validate_signature(body, signature, settings.amo_secret):
        raise HTTPException(status_code=403, detail="invalid signature")
    payload = await request.json()
    chat_id, text = parse_incoming(payload)
    await handle_intent(chat_id, text)
    return {"status": "accepted"}


@app.post("/kb/reindex")
async def kb_reindex() -> dict[str, str]:
    """Trigger knowledge base reindexing."""
    await reindex_kb()
    return {"status": "queued"}
