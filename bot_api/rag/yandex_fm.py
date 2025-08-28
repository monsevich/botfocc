"""Async client for Yandex Foundation Models."""
from typing import Iterable, List

import httpx


class YandexFoundationModel:
    """Minimal wrapper around Yandex Foundation Models API."""

    def __init__(self, api_key: str, folder_id: str) -> None:
        self._client = httpx.AsyncClient(base_url="https://llm.api.cloud.yandex.net")
        self._headers = {"Authorization": f"Api-Key {api_key}", "x-folder-id": folder_id}

    async def embed(self, texts: Iterable[str]) -> List[List[float]]:
        """Return embedding vectors for provided texts."""
        resp = await self._client.post(
            "/foundationModels/v1/embeddings",
            json={"texts": list(texts)},
            headers=self._headers,
        )
        resp.raise_for_status()
        return resp.json().get("vectors", [])

    async def generate(self, system: str, context: str, user: str) -> str:
        """Generate completion given system prompt, context and user input."""
        payload = {
            "model": "yandexgpt-lite",
            "messages": [
                {"role": "system", "text": system},
                {"role": "user", "text": f"{context}\n{user}"},
            ],
        }
        resp = await self._client.post(
            "/foundationModels/v1/completion", json=payload, headers=self._headers
        )
        resp.raise_for_status()
        return (
            resp.json()
            .get("result", {})
            .get("alternatives", [{}])[0]
            .get("message", {})
            .get("text", "")
        )
