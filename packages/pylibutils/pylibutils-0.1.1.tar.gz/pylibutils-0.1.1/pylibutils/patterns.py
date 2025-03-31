from threading import Lock
from typing import Any


class Singleton:
    """A simple thread-safe singleton pattern."""

    _instance: Any = None
    _lock = Lock()

    def __new__(cls, **kwargs):
        """Implement thread-safe singleton behavior."""

        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)

        return cls._instance
