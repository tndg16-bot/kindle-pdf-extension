"""Shared helpers for login password generation.

Passwords rotate daily at 09:00 JST. Before 09:00 we keep the previous day's
password so early-morning users are not locked out.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timedelta
from typing import Tuple

try:  # Python 3.9+
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore

JST = ZoneInfo("Asia/Tokyo") if ZoneInfo is not None else None


def _now_jst(now: datetime | None = None) -> datetime:
    """Return the current time as a timezone-aware datetime in JST."""
    if now is None:
        if JST is not None:
            return datetime.now(JST)
        return datetime.now()  # Fallback (should not happen on py3.11)
    if JST is None:
        return now
    if now.tzinfo is None:
        return now.replace(tzinfo=JST)
    return now.astimezone(JST)


def _effective_date(now: datetime | None = None) -> datetime:
    """Date (JST) that determines today's password."""
    current = _now_jst(now)
    if current.hour < 9:
        current -= timedelta(days=1)
    return current


def get_current_password(now: datetime | None = None) -> str:
    """Return the password string for the effective JST date."""
    _, password = get_password_parts(now)
    return password


def get_password_parts(now: datetime | None = None) -> Tuple[str, str]:
    """Return `(date_key, password)` pair used across the system."""
    current = _effective_date(now)
    date_key = current.strftime("%Y-%m-%d")
    seed = f"MojiBooster_{date_key}_Daily"
    hex_dig = hashlib.sha256(seed.encode()).hexdigest()[:16]
    password = f"Moji{hex_dig[:4].upper()}{hex_dig[4:8].lower()}"
    return date_key, password


def describe_password(now: datetime | None = None) -> dict:
    """Convenience helper for tests and templates."""
    current = _now_jst(now)
    date_key, password = get_password_parts(now)
    return {
        "effective_date": date_key,
        "password": password,
        "now_jst": current,
    }

