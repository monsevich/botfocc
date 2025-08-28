"""Helpers for interacting with amoCRM."""
import hashlib, hmac, httpx, time, email.utils
from typing import Tuple
from .settings import Settings

def parse_incoming(payload: dict) -> Tuple[str, str]:
    # v2 hook: message.conversation.id / message.message.text
    msg = payload.get("message", {})
    conv = msg.get("conversation", {}) or {}
    chat_id = conv.get("id", "")
    text = (msg.get("message", {}) or {}).get("text", "") or ""
    return chat_id, text

async def send_reply(settings: Settings, conversation_id: str, text: str) -> None:
    """
    POST /v2/origin/custom/{scope_id}
    Headers: Date, Content-Type, Content-MD5, X-Signature (HMAC-SHA1 over canonical string)
    """
    base = settings.amo_base_url.rstrip("/")
    path = f"/v2/origin/custom/{settings.amo_scope_id}"
    url = f"{base}{path}"
    body = {
        "payload": {
            "timestamp": int(time.time()),
            "event_type": "new_message",
            "conversation_id": conversation_id,
            "sender": {"id": "bot"},      # можно подменить на ID бота интеграции
            "receiver": {"id": "client"}, # amo подставит фактические id
            "message": {"type": "text", "text": text},
        }
    }
    import json
    content_type = "application/json"
    request_body = json.dumps(body, ensure_ascii=False)
    content_md5 = hashlib.md5(request_body.encode("utf-8")).hexdigest()
    date_hdr = email.utils.formatdate(usegmt=True)

    canonical = "\n".join(["POST", content_md5, content_type, date_hdr, path])
    signature = hmac.new(
        settings.amo_secret.encode("utf-8"), canonical.encode("utf-8"), hashlib.sha1
    ).hexdigest()

    headers = {
        "Date": date_hdr,
        "Content-Type": content_type,
        "Content-MD5": content_md5,
        "X-Signature": signature,
    }

    async with httpx.AsyncClient(timeout=5) as cli:
        r = await cli.post(url, headers=headers, content=request_body)
        r.raise_for_status()
