import random
import string
from datetime import datetime, timedelta, timezone
from typing import Optional

_CHARS = string.ascii_lowercase + string.digits  # a-z0-9


def generate_alias(length: int = 6) -> str:
    """Generate a random URL-safe alias."""
    return "".join(random.choices(_CHARS, k=length))


def compute_expiry(expires_in_days: Optional[int]) -> Optional[datetime]:
    """Return a UTC-aware expiry datetime, or None if no expiry."""
    if expires_in_days is None:
        return None
    return datetime.now(timezone.utc) + timedelta(days=expires_in_days)


def is_expired(expires_at: Optional[str | datetime]) -> bool:
    """Return True if the link has passed its expiry date."""
    if expires_at is None:
        return False
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    # Make timezone-aware if naive
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) > expires_at