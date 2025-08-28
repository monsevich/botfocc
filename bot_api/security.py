"""Signature helpers for amoCRM webhooks."""
import hmac
import hashlib


def sign(payload: bytes, secret: str) -> str:
    """Return hex digest of HMAC-SHA256 signature."""
    return hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()


def validate_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Validate provided signature against payload and secret."""
    expected = sign(payload, secret)
    return hmac.compare_digest(expected, signature)
