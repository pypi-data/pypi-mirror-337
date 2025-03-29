from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class PriceTypeEnumeration(Enumeration):
    """Enumerates different price types, for example list price, invoice price, and sale price."""
    type: str = field(default_factory=lambda: "PriceTypeEnumeration", name="@type")