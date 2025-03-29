from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class PublicationVolume(CreativeWork):
    """A part of a successively published publication such as a periodical or multi-volume work, often numbered. It may represent a time span, such as a year.\\n\\nSee also [blog post](https://blog-schema.org/2014/09/02/schema-org-support-for-bibliographic-relationships-and-periodicals/)."""
    type: str = field(default_factory=lambda: "PublicationVolume", name="@type")
    pageEnd: int | str | None = None
    pagination: str | None = None
    volumeNumber: int | str | None = None
    pageStart: int | str | None = None