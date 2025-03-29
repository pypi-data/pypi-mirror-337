from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class DataFeedItem(Intangible):
    """A single item within a larger data feed."""
    type: str = field(default_factory=lambda: "DataFeedItem", name="@type")
    dateModified: datetime | date | None = None
    dateDeleted: datetime | date | None = None
    dateCreated: datetime | date | None = None
    item: 'Thing' | None = None