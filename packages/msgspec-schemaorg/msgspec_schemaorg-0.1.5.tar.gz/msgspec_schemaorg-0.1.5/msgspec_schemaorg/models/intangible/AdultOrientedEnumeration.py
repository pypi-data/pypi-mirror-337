from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class AdultOrientedEnumeration(Enumeration):
    """Enumeration of considerations that make a product relevant or potentially restricted for adults only."""
    type: str = field(default_factory=lambda: "AdultOrientedEnumeration", name="@type")