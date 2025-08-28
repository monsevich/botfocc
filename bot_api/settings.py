"""Application settings loaded from Yandex Lockbox at runtime."""
from pydantic import BaseModel


class Settings(BaseModel):
    """Names of required configuration keys.

    Actual values are fetched from Yandex Lockbox via instance metadata on
    startup. Secrets are not stored in the repository.
    """

    database_dsn: str
    amo_secret: str
    amo_base_url: str
    yfm_api_key: str
    yfm_folder_id: str
    kb_path: str
    qdrant_url: str
    qdrant_api_key: str
