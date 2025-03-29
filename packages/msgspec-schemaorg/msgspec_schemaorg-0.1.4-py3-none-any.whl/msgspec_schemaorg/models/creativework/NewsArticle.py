from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Article import Article
from typing import Optional, Union, Dict, List, Any


class NewsArticle(Article):
    """A NewsArticle is an article whose content reports news, or provides background context and supporting materials for understanding the news.

A more detailed overview of [schema.org News markup](/docs/news.html) is also available.
"""
    type: str = field(default_factory=lambda: "NewsArticle", name="@type")
    printSection: str | None = None
    dateline: str | None = None
    printColumn: str | None = None
    printPage: str | None = None
    printEdition: str | None = None