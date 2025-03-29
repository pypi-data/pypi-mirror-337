from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Chapter(CreativeWork):
    """One of the sections into which a book is divided. A chapter usually has a section number or a name."""
    type: str = field(default_factory=lambda: "Chapter", name="@type")
    pageEnd: int | str | None = None
    pagination: str | None = None
    pageStart: int | str | None = None