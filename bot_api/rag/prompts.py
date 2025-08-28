"""Prompt builders for RAG generation."""
from typing import Iterable


def system_prompt(tone: str, disclaimers: Iterable[str], escalation: str) -> str:
    """Compose system prompt string."""
    lines = [f"You are a {tone} assistant for a cosmetology clinic."]
    lines.extend(disclaimers)
    lines.append(f"If unsure, escalate to {escalation}.")
    return "\n".join(lines)
