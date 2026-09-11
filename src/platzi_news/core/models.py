"""Data models for Platzi News."""

from dataclasses import dataclass


@dataclass
class Article:
    """Represents a news article."""

    title: str
    description: str
    url: str

    def get(self, key: str, default=None):
        return getattr(self, key, default)
