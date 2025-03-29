from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class PriceComponentTypeEnumeration(Enumeration):
    """Enumerates different price components that together make up the total price for an offered product."""
    type: str = field(default_factory=lambda: "PriceComponentTypeEnumeration", name="@type")