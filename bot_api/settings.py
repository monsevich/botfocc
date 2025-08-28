"""Application settings loaded from Yandex Lockbox at runtime."""
from pydantic import BaseModel
import os, httpx

class Settings(BaseModel):
    database_dsn: str
    amo_secret: str
    amo_base_url: str
    amo_scope_id: str
    amo_account_id: str
    yfm_api_key: str
    yfm_folder_id: str
    kb_path: str | None = None
    qdrant_url: str
    qdrant_api_key: str | None = None

def _metadata_iam_token() -> str:
    url = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
    headers = {"Metadata-Flavor": "Google"}
    r = httpx.get(url, headers=headers, timeout=2)
    r.raise_for_status()
    return r.json()["access_token"]

def _load_from_lockbox(secret_id: str) -> dict[str, str]:
    token = _metadata_iam_token()
    url = f"https://payload.lockbox.api.cloud.yandex.net/lockbox/v1/secrets/{secret_id}/payload"
    r = httpx.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=3)
    r.raise_for_status()
    items = r.json().get("entries", [])
    out = {}
    for it in items:
        key = it["key"]
        tv = it.get("textValue")
        bv = it.get("binaryValue")
        out[key] = tv if tv is not None else (bv or "")
    return out

def load_settings() -> Settings:
    secret_id = os.getenv("LOCKBOX_SECRET_ID")
    if secret_id:
        data = _load_from_lockbox(secret_id)
        return Settings(**data)
    # fallback для локалки
    return Settings(
        database_dsn=os.environ["DATABASE_DSN"],
        amo_secret=os.environ["AMO_SECRET"],
        amo_base_url=os.environ.get("AMO_BASE_URL","https://amojo.amocrm.ru"),
        amo_scope_id=os.environ["AMO_SCOPE_ID"],
        amo_account_id=os.environ["AMO_ACCOUNT_ID"],
        yfm_api_key=os.environ["YFM_API_KEY"],
        yfm_folder_id=os.environ["YFM_FOLDER_ID"],
        kb_path=os.environ.get("KB_PATH", "/app/kb_files"),
        qdrant_url=os.environ["QDRANT_URL"],
        qdrant_api_key=os.environ.get("QDRANT_API_KEY",""),
    )
