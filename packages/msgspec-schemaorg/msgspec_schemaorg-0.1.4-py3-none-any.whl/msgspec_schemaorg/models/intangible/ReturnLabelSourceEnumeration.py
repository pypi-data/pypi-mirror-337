from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class ReturnLabelSourceEnumeration(Enumeration):
    """Enumerates several types of return labels for product returns."""
    type: str = field(default_factory=lambda: "ReturnLabelSourceEnumeration", name="@type")