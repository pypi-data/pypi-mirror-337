from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class ItemListOrderType(Enumeration):
    """Enumerated for values for itemListOrder for indicating how an ordered ItemList is organized."""
    type: str = field(default_factory=lambda: "ItemListOrderType", name="@type")