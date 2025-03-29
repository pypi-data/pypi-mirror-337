from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.intangible.SpeakableSpecification import SpeakableSpecification
from typing import Optional, Union, Dict, List, Any


class Article(CreativeWork):
    """An article, such as a news article or piece of investigative report. Newspapers and magazines have articles of many different types and this is intended to cover them all.\\n\\nSee also [blog post](http://blog.schema.org/2014/09/schemaorg-support-for-bibliographic_2.html)."""
    type: str = field(default_factory=lambda: "Article", name="@type")
    pageEnd: int | str | None = None
    speakable: 'URL' | 'SpeakableSpecification' | None = None
    backstory: str | 'CreativeWork' | None = None
    articleSection: str | None = None
    pagination: str | None = None
    wordCount: int | None = None
    articleBody: str | None = None
    pageStart: int | str | None = None