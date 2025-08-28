"""Async client for Yandex Foundation Models."""
import httpx
from typing import Iterable, List

class YandexFoundationModel:
    def __init__(self, api_key: str, folder_id: str) -> None:
        self._client = httpx.AsyncClient(base_url="https://llm.api.cloud.yandex.net")
        self._headers = {"Authorization": f"Api-Key {api_key}"}
        self._folder_id = folder_id
        self._model_uri = f"gpt://{folder_id}/yandexgpt-lite/latest"
        self._embed_model_uri = f"emb://{folder_id}/text-search/latest"  # пример, подберите под вашу нужду

    async def embed(self, texts: Iterable[str]) -> List[List[float]]:
        vecs: List[List[float]] = []
        for t in texts:
            resp = await self._client.post(
                "/foundationModels/v1/textEmbedding",
                json={"modelUri": self._embed_model_uri, "text": t},
                headers=self._headers,
            )
            resp.raise_for_status()
            vecs.append(resp.json()["embedding"])
        return vecs

    async def generate(self, system: str, context: str, user: str) -> str:
        payload = {
            "modelUri": self._model_uri,
            "completionOptions": {"temperature": 0.3, "maxTokens": "800"},
            "messages": [
                {"role": "system", "text": system},
                {"role": "user", "text": f"{context}\n\nПользователь: {user}"},
            ],
        }
        resp = await self._client.post("/foundationModels/v1/completion", json=payload, headers=self._headers)
        resp.raise_for_status()
        alts = resp.json().get("alternatives", [])
        return (alts[0].get("message", {}) or {}).get("text", "") if alts else ""
