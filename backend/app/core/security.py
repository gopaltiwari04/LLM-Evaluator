import hashlib
import secrets


API_KEY_PREFIX = "llmo_live_"


def generate_api_key() -> tuple[str, str]:
    """
    Generate a raw API key and its SHA-256 hash.

    The raw key is returned once to the caller.
    Only the hash should be stored in the database.
    """
    random_part = secrets.token_urlsafe(32)

    raw_key = f"{API_KEY_PREFIX}{random_part}"

    key_hash = hashlib.sha256(
        raw_key.encode("utf-8")
    ).hexdigest()

    return raw_key, key_hash


def hash_api_key(api_key: str) -> str:
    """Hash an API key for lookup."""
    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()