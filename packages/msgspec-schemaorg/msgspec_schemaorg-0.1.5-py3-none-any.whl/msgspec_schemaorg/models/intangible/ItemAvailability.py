from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class ItemAvailability(Enumeration):
    """A list of possible product availability options."""
    type: str = field(default_factory=lambda: "ItemAvailability", name="@type")