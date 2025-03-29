from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class PurchaseType(Enumeration):
    """Enumerates a purchase type for an item."""
    type: str = field(default_factory=lambda: "PurchaseType", name="@type")