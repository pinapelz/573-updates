from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from scrapers.base import NewsSource

_registry: dict[str, type["NewsSource"]] = {}


def register(url_key: str):
    def decorator(cls):
        _registry[url_key] = cls
        return cls
    return decorator


def get_source(url_key: str) -> Optional[type["NewsSource"]]:
    return _registry.get(url_key)


def get_all() -> dict[str, type["NewsSource"]]:
    return dict(_registry)
