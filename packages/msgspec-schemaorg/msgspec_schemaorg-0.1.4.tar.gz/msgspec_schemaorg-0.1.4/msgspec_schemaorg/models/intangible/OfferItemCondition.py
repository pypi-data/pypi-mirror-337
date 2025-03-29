from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class OfferItemCondition(Enumeration):
    """A list of possible conditions for the item."""
    type: str = field(default_factory=lambda: "OfferItemCondition", name="@type")