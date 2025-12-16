"""
Helpers to bind Gradio session tokens to the current rotating password.

We replace Gradio's internal `App.tokens` dictionary with a custom store
that remembers the password `effective_date` at the moment a token is issued.
Whenever a request retrieves a token (via `dict.get` / `__getitem__` / etc.),
we compare the stored date with today's effective date (09:00 JST cutover).
If they differ, the token is purged so the user is forced back to the login
screen, matching the dynamic password schedule.
"""

from __future__ import annotations

import threading
from collections.abc import Iterable, Mapping
from typing import Any, Hashable

from .password_utils import describe_password

_INSTALL_LOCK = threading.Lock()
_INSTALLED = False


def _current_effective_date() -> str:
    """Return the current effective date string (YYYY-MM-DD, JST-based)."""
    info = describe_password()
    return info["effective_date"]


class PasswordBoundTokenStore(dict[str, str]):
    """
    Dict-like store that invalidates tokens whenever the password rolls over.

    Keys are the opaque Gradio session tokens; values remain the username
    strings expected by Gradio. Metadata about the effective date is tracked
    internally so stale tokens can be evicted transparently.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()
        self._lock = threading.RLock()
        self._issued_date: dict[str, str] = {}
        if args or kwargs:
            self.update(*args, **kwargs)

    # ---- Core helpers -------------------------------------------------

    def _record_issue(self, token: str) -> None:
        self._issued_date[token] = _current_effective_date()

    def _purge(self, token: str) -> None:
        super().pop(token, None)
        self._issued_date.pop(token, None)

    def _ensure_fresh(self, token: str) -> None:
        recorded = self._issued_date.get(token)
        if recorded is None:
            return
        if recorded != _current_effective_date():
            self._purge(token)

    # ---- Dict API overrides -------------------------------------------

    def __setitem__(self, token: str, username: str) -> None:
        with self._lock:
            self._record_issue(token)
            super().__setitem__(token, username)

    def __getitem__(self, token: Hashable) -> str:  # type: ignore[override]
        with self._lock:
            if isinstance(token, str):
                self._ensure_fresh(token)
            return super().__getitem__(token)

    def __contains__(self, token: object) -> bool:
        with self._lock:
            if isinstance(token, str):
                self._ensure_fresh(token)
            return super().__contains__(token)

    def get(self, token: Hashable, default: Any = None) -> Any:  # type: ignore[override]
        with self._lock:
            if isinstance(token, str):
                self._ensure_fresh(token)
            return super().get(token, default)

    def pop(self, token: Hashable, default: Any = None) -> Any:  # type: ignore[override]
        with self._lock:
            if isinstance(token, str):
                self._issued_date.pop(token, None)
            return super().pop(token, default)

    def popitem(self) -> tuple[str, str]:
        with self._lock:
            token, username = super().popitem()
            self._issued_date.pop(token, None)
            return token, username

    def clear(self) -> None:
        with self._lock:
            super().clear()
            self._issued_date.clear()

    def setdefault(self, token: str, default: str) -> str:
        with self._lock:
            if token not in self:
                self._record_issue(token)
            return super().setdefault(token, default)

    def update(self, *args: Any, **kwargs: Any) -> None:
        with self._lock:
            if args:
                (arg,) = args
                if isinstance(arg, Mapping):
                    for token, username in arg.items():
                        self._record_issue(token)
                        super().__setitem__(token, username)
                elif isinstance(arg, Iterable):
                    for token, username in arg:
                        self._record_issue(token)
                        super().__setitem__(token, username)
                else:
                    raise TypeError("update() requires a mapping or iterable of pairs")
            for token, username in kwargs.items():
                self._record_issue(token)
                super().__setitem__(token, username)

    def keys(self):
        with self._lock:
            stale = [token for token in self._issued_date if token not in super().keys()]
            for token in stale:
                self._issued_date.pop(token, None)
            tokens = list(super().keys())
            for token in tokens:
                self._ensure_fresh(token)
            return super().keys()

    # -------------------------------------------------------------------


def install_token_guard() -> None:
    """
    Patch Gradio's App class so all future instances use the guarded token store.
    """
    global _INSTALLED
    with _INSTALL_LOCK:
        if _INSTALLED:
            return

        import gradio.routes  # Imported lazily to keep startup costs low

        original_init = gradio.routes.App.__init__

        def patched_init(self, *args: Any, **kwargs: Any) -> None:  # type: ignore[override]
            original_init(self, *args, **kwargs)
            self.tokens = PasswordBoundTokenStore(self.tokens)

        gradio.routes.App.__init__ = patched_init  # type: ignore[assignment]
        _INSTALLED = True

