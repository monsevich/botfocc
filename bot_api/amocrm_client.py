"""Helpers for interacting with amoCRM."""
from typing import Tuple


async def send_reply(chat_id: str, text: str) -> None:
    """Send a reply message to amoCRM chat.

    Example request::

        POST /api/v4/chats/messages
        {"chat_id": "123", "text": "Hello"}
    """
    # HTTP request placeholder
    return None


def parse_incoming(payload: dict) -> Tuple[str, str]:
    """Extract chat ID and text from amoCRM webhook payload."""
    message = payload.get("message", {})
    return message.get("chat_id", ""), message.get("text", "")
