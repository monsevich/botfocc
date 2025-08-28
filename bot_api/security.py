"""Signature helpers for amoCRM webhooks."""
 import hmac, hashlib

def sign_sha1(payload: bytes, secret: str) -> str:
    return hmac.new(secret.encode(), payload, hashlib.sha1).hexdigest()

def validate_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = sign_sha1(payload, secret)
    return hmac.compare_digest(expected, signature.lower())
