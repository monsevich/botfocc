"""High level dialog orchestration."""
from typing import List

from qdrant_client import AsyncQdrantClient

from ..amocrm_client import send_reply
from ..settings import Settings
from ..db import pg
from ..rag.yandex_fm import YandexFoundationModel
from ..rag.retriever import retrieve
from ..rag.prompts import system_prompt

INTENTS = [
    "booking",
    "info",
    "price",
    "contra",
    "transfer",
    "address",
    "other",
]


async def handle_intent(chat_id: str, text: str) -> None:
    """Process message, generate reply and send back to amoCRM.

    Booking intent should populate amoCRM fields and tags expected by existing
    YCLIENTS integration. Low-confidence answers should be escalated to a human.
    """
    settings: Settings = pg.settings
    yfm = YandexFoundationModel(settings.yfm_api_key, settings.yfm_folder_id)
    qdrant = AsyncQdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
    docs = await retrieve(text, yfm, qdrant)
    context = "\n".join(d[0] for d in docs)
    system = system_prompt(
        tone="friendly",
        disclaimers=["Information is not medical advice."],
        escalation="operator",
    )
    reply = await yfm.generate(system, context, text)
    await send_reply(chat_id, reply)
